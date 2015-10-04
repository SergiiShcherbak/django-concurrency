# -*- coding: utf-8 -*-
from django.test.utils import override_settings
import pytest

from concurrency.api import disable_concurrency, _thread_locals
from concurrency.exceptions import RecordModifiedError
from concurrency.utils import refetch
from demo.models import AutoIncConcurrentModel, SimpleConcurrentModel
from demo.util import nextname


@pytest.mark.django_db(transaction=False)
def test_disable_concurrency_settings(settings):
    with override_settings(CONCURRENCY_ENABLED=False):
        instance1 = SimpleConcurrentModel(username=next(nextname))
        instance1.save()
        refetch(instance1).save()


@pytest.mark.django_db(transaction=False)
def test_disable_concurrency_global():
    instance1 = SimpleConcurrentModel(username=next(nextname))
    instance2 = AutoIncConcurrentModel(username=next(nextname))
    instance1.save()
    instance2.save()
    refetch(instance1).save()
    refetch(instance2).save()
    with disable_concurrency():
        instance1.save()
        instance2.save()

    copy2 = refetch(instance2)
    refetch(instance2).save()
    with pytest.raises(RecordModifiedError):
        copy2.save()


@pytest.mark.django_db(transaction=False)
def test_disable_concurrency(model_class=SimpleConcurrentModel):
    instance = model_class(username=next(nextname))
    instance.save()
    copy = refetch(instance)
    copy.save()
    with disable_concurrency(SimpleConcurrentModel):
        instance.save()


@pytest.mark.django_db(transaction=False)
def test_disable_concurrency_specific_model(model_class=SimpleConcurrentModel):
    instance1 = model_class(username=next(nextname))
    instance1.save()
    copy1 = refetch(instance1)
    copy1.save()

    instance2 = model_class(username=next(nextname))
    instance2.save()
    copy2 = refetch(instance2)
    copy2.save()

    with disable_concurrency(instance1):
        instance1.save()
        with pytest.raises(RecordModifiedError):
            instance2.save()
