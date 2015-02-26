from django.middleware import transaction

from contextlib import contextmanager


@contextmanager
def without_signals(*disablers):
    for disabler in disablers:
        if not (isinstance(disabler, list) or isinstance(disabler, tuple)) or len(disabler) == 0:
            raise ValueError("The parameters must be lists of at least one parameter (the signal)")

        signal, ids = disabler
        signal.backup_receivers = signal.receivers
        signal.receivers = list(filter(lambda x: x[0][0] not in ids, signal.receivers))

    try:
        yield
    except Exception as e:
        raise e
    finally:
        for disabler in disablers:
            signal, ids = disabler
            signal.receivers = signal.backup_receivers

