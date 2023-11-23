import pytest
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed
)

@pytest.fixture(autouse=True)
def mute_signals(request):
    if 'enable_signals' in request.keywords:
        return

    signals = [
        pre_save,
        post_save,
        pre_delete,
        post_delete,
        m2m_changed
    ]
    restore = {}
    for signal in signals:
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        for signal, receivers in restore.items():
            signal.receivers = receivers

    request.addfinalizer(restore_signals)