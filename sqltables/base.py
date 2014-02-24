# -*- coding: utf-8 -*-

from django.utils import six

from functools import update_wrapper
import json, re
from django.http import HttpResponse
from .filters import TextFilter,SelectFilter,NumberFilter,NumberRangeFilter,DateRangeFilter

from django.db import DatabaseError

class TableMeta(type):
    """
    Metaclass for all tables. Maybe not needed.
    """
    pass

class Table(six.with_metaclass(TableMeta)):

    def __init__(self, manager):
        self.query_parameters = []
        self.filtering_enabled = False
        self.paging = True
        self.export_file_name = None
        self.manager = manager

        if not self.query_parameters:
            # find named placeholders
            self.query_parameters = re.findall('%\(([^)]*)\)s',self.get_query())
        if not self.export_file_name:
            self.export_file_name = self.__class__.__name__.lower()+'.csv'

        self.m_columns=getattr(self, 'columns', None)
        if not self.m_columns:
            self.m_columns=self.detect_columns()

    def detect_columns(self):
        q = "SELECT * FROM ({q}) AS q LIMIT 0".format(q=self.query)
        c = self.get_cursor()
        columns=[]
        try:
            c.execute(q,{p:'0' for p in self.query_parameters})
            for col in c.description:
                columns.append({
                    'name': col[0],
                    'label': col[0],
                    })
        finally:
            c.close()
        return columns


    def get_path(self):
        return self.__module__.split('.')[-2], self.__class__.__name__

    def get_query(self):
        return self.query

    def get_cursor(self):
        from django.db import connection, connections
        try:
            return connections[self.connection_name].cursor()
        except AttributeError:
            pass
        
        return connection.cursor()

    def get_urls(self):
        from django.conf.urls import patterns, url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.manager.manager_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('',
                url(r'^definition$',
                    self.definition_view,
                    name='%s_%s_definition' % self.get_path()
                ),
                url(r'^data$',
                    self.data_view,
                    name='%s_%s_data' % self.get_path()
                ),
                url(r'^csv$',
                    self.csv_view,
                    name='%s_%s_csv' % self.get_path()
                ),
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    #
    # Return table definition for JavaScript processing
    #
    def definition_view(self, request):
        rv_c=[]
        for c in self.m_columns:
            d={'name': c['name']}
            try:
                d['label']=c['label']
            except KeyError:
                d['label']=c['name']
            if self.filtering_enabled:
                try:
                    d['filter']={'type': c['filter'].get_type()}
                    d['filter'].update(c['filter'].get_js_attrs())
                except KeyError:
                    pass
            rv_c.append(d)

        res={
                'columns': rv_c,
                'filtering_enabled': self.filtering_enabled,
                'paging': self.paging,
                'default_sort_by': self.m_columns[0]['name'],
        }

        if self.query_parameters:
            res['params'] = self.query_parameters

        try:
            res['caption'] = self.caption
        except AttributeError:
            pass

        return HttpResponse(
                json.dumps(res),
                content_type="application/json")

    def build_select_list(self):
        return ", ".join([c['name'] for c in self.m_columns])

    def get_data(self, request, limit=True):
        # get parameters values from request
        q_params={}
        try:
            for p in self.query_parameters:
                q_params[p]=request.GET["param_"+p]
        except KeyError:
            raise                       # FIXME FIXME FIXME

        

        # build WHERE part
        q_where_str=""
        if self.filtering_enabled:
            q_where=[]
            for i, c in enumerate(self.m_columns):
                try:
                    expression, params = c['filter'].get_filter_expression(request, c['name'], i)
                    if expression is not None:
                        q_params.update(params)
                        q_where.append('({})'.format(expression))
                except KeyError:
                    pass
            if q_where:
                q_where_str="WHERE %s" % (" AND ".join(q_where))

        # build ORDER BY part
        q_order_by=[]
        for col in self.m_columns:
            if col['name']==request.GET['sidx']:
                order=('ASC', 'DESC')[request.GET['sord']=='desc']
                try:
                    col_name=col['order_by']
                except KeyError:
                    col_name=col['name']
                q_order_by.append("{} {}".format(col_name, order))

#        for i in range(int(request.GET['iSortingCols'])):
#            col=self.m_columns[int(request.GET['iSortCol_%d' % i])]
#            order=('ASC', 'DESC')[request.GET['sSortDir_%d' % i]=='desc']
#            try:
#                col_name=col['order_by']
#            except KeyError:
#                col_name=col['name']
#            q_order_by.append("%s %s" % (col_name, order))

        q_order_by_str=""
        if q_order_by:
            q_order_by_str="ORDER BY %s" % (", ".join(q_order_by))


        # build LIMIT/OFFSET part
        limit_q=""
        if limit:
            try:
                q_params['_limit_limit']=int(request.GET['rows'])
                q_params['_limit_offset']=(int(request.GET['page'])-1)*int(request.GET['rows'])
                limit_q="LIMIT %(_limit_limit)s OFFSET %(_limit_offset)s"
                if q_params['_limit_limit']<0:
                    limit_q=""
            except KeyError:
                pass

        sl=self.build_select_list()
        q="SELECT %s FROM (%s) AS t %s %s %s" % (sl, self.query,
                q_where_str, q_order_by_str, limit_q)

        print q

        cursor=self.get_cursor()
        #from pprint import pprint
        #pprint(q)
        #pprint(q_params)
        cursor.execute(q, q_params)
        return cursor

    def data_view(self, request):

        cursor=self.get_data(request,True)

        res=[]
        for row in cursor.fetchall():
            t=[]
            for x in row:
                t.append(unicode(x))
            res.append(t)

        #total  total pages for the query
        #page    current page of the query
        #records total number of records for the query
        d={"rows": res,}
        try:
            d['sEcho']=int(request.GET['sEcho'])
        except KeyError:
            pass
        return HttpResponse(json.dumps(d),
                content_type="application/json")


    def csv_view(self, request):

        cursor=self.get_data(request,False)


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.export_file_name)

        #import csv
        import unicodecsv
        #writer = csv.writer(response)
        writer = unicodecsv.writer(response)

        t=[]
        for c in self.m_columns:
            try:
                t.append(c['label'])
            except KeyError:
                t.append(c['name'])
        writer.writerow(t)
        for row in cursor.fetchall():
            t=[]
            for x in row:
                t.append(unicode(x))
            writer.writerow(t)

        return response

