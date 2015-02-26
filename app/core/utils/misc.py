__all__ = [
    'Hider',
    'check_dependencies',
    'choicify',
    'get_key_by_value',
]

# Django imports

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


from ..exceptions import DependencyError



class Hider(object):
    def __get__(self,instance,owner):
        raise AttributeError("Hidden attrbute")

    def __set__(self, obj, val):
        raise AttributeError("Hidden attribute")


def check_dependencies(dependencies, module):
    """
    Ensure dependencies of a module are listed in settings.INSTALLED_APPS
    
    :dependencies string | list: list of dependencies to check
    :module string: string representing the path to the current app
    """
    if type(dependencies) == str:
        dependencies = [dependencies]
    elif type(dependencies) != list:
        raise TypeError('dependencies argument must be of type list or string')
    
    for dependency in dependencies:
        if dependency not in settings.INSTALLED_APPS:
            raise DependencyError('%s depends on %s, which should be in settings.INSTALLED_APPS' % (module, dependency))


def choicify(dictionary):
    """
    Converts a readable python dictionary into a django model/form
    choice structure (list of tuples) ordered based on the values of each key
    
    :param dictionary: the dictionary to convert
    """
    # get order of the fields
    ordered_fields = sorted(dictionary, key=dictionary.get)
    choices = []
    # loop over each field
    for field in ordered_fields:
        # build tuple (value, i18n_key)
        row = (dictionary[field], _(field.replace('_', ' ')))
        # append tuple to choices
        choices.append(row)
    # return django sorted choices
    return choices


def get_key_by_value(dictionary, search_value):
    """
    searchs a value in a dicionary and returns the key of the first occurrence
    
    :param dictionary: dictionary to search in
    :param search_value: value to search for
    """
    for key, value in dictionary.iteritems():
        if value == search_value:
            return ugettext(key)


def pause_disconnectable_signals():
    """
    Disconnects non critical signals like notifications, websockets and stuff like that.
    Use when managing large chunks of nodes
    """
    for signal in DISCONNECTABLE_SIGNALS:
        signal['disconnect']()


def resume_disconnectable_signals():
    """
    Reconnects non critical signals like notifications, websockets and stuff like that.
    Use when managing large chunks of nodes
    """
    for signal in DISCONNECTABLE_SIGNALS:
        signal['reconnect']()


