# -*- coding: utf-8 -*-

#
#
# 
# $("#tableId").dataTable().columnFilter(
#               {
#                     aoColumns: [
#                                    {
#                                         type: "number"
#                                    },
#                                    {
#                                         type: "text",
#                                         bRegex: true,
#                                         bSmart: true
#                                    },
#                                    null,
#                                    {
#                                         type: "select",
#                                         values: [ 'A', 'B', 'C' ]
#                                    },
#                                    {
#                                         type: "number-range"
#                                    },
#                                    {
#                                         type: "date-range"
#                                    }
#                                 ]
#               }
# );
#If you pass aoColumn array with definition of the individual column filters you can customize behavior of the filters. The most important setting is type that can define how filtering will be done. Possible values are:
#
#text - default behavior. You can define whether the regular expression or smart filtering will be used in the filtering,
#number - filter numbers in the column,
#select - put the select list that will be used for filtering. Values of the items in the list are placed in the values array,
#null - do not add filter in the column,
#number range - add two from-to filters to filter the number in the range,
#date-range - add two from-to calendar to filter the dates in the range.

class FieldFilter(object):
    def get_type(self):
        return None

    def get_js_attrs(self):
        return {}

    def get_filter_expression(self, request, column_name, column_id):
        return (None,{})  # Empty query, empty parameter dict

class TextFilter(FieldFilter):
    def get_type(self):
        return 'text'
    def get_filter_expression(self, request, column_name, column_id):
        search=request.GET['sSearch_{}'.format(column_id)]
        if search=='':
            return (None,{})

        param_name='search_{}'.format(column_id)

        return ('{}::text ILIKE %({})s'.format(column_name,param_name),
                {param_name: u'%{}%'.format(search)})


class SelectFilter(FieldFilter):
    def __init__(self, values):
        self.values=values
    def get_type(self):
        return 'select'
    def get_js_attrs(self):
        return {'values': self.values}
    def get_filter_expression(self, request, column_name, column_id):
        search=request.GET['sSearch_{}'.format(column_id)]
        if search=='':
            return (None,{})

        param_name='search_{}'.format(column_id)

        return ('{} = %({})s'.format(column_name,param_name),
                {param_name: search})

class NumberFilter(FieldFilter):
    def get_type(self):
        return 'number'

class NumberRangeFilter(FieldFilter):
    def get_type(self):
        return 'number-range'

class DateRangeFilter(FieldFilter):
    def get_type(self):
        return 'date-range'
