# -*- coding: utf-8 -*-

__version__ = '0.1.0'

from sqltables.manager import manager

#
# Code heavily inspred by django.contrib.admin
#

def autodiscover():
    """
    Auto-discover INSTALLED_APPS tables.py modules and fail silently when
    not present. This forces an import on them to register any tables bits they
    may want.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's tables module.
        try:
            before_import_registry = copy.copy(manager._registry)
            import_module('%s.tables' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            manager._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an tables module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'tables'):
                raise
