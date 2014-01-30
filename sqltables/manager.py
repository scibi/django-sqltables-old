from django.utils import six

from .base import TableMeta

class AlreadyRegistered(Exception):
    pass



class Manager(object):
    def __init__(self, ):
        self._registry = {}

    def register(self, table_or_iterable):
        if isinstance(table_or_iterable, TableMeta):
            table_or_iterable = [table_or_iterable]

        for table in table_or_iterable:

            if table in self._registry:
                raise AlreadyRegistered('The table %s is already registered' %
                        table.__name__)

            self._registry[table]=table(self)

    def get_urls(self):
        from django.conf.urls import patterns, url, include

        urlpatterns = patterns('')

        for table_class, table_object in six.iteritems(self._registry):
            urlpatterns += patterns('', url(r'^%s/%s/' % table_object.get_path(),
                include(table_object.urls)))


        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'tables', 'tables'



manager = Manager()
