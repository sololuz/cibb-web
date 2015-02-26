# -*- encoding:utf-8 -*-

from django.template.defaultfilters import slugify

import time

from unidecode import unidecode


def slugify_uniquely(value, model, slugfield="slug"):
    """
    Returns a slug on a name which is unique within a model's table
    """

    suffix = 0
    potential = base = slugify(unidecode(value))
    if len(potential) == 0:
        potential = 'null'
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).exists():
            return potential
        suffix += 1


def slugify_uniquely_for_queryset(value, queryset, slugfield="slug"):
    """
    Returns a slug on a name which doesn't exist in a queryset
    """

    suffix = 0
    potential = base = slugify(unidecode(value))
    if len(potential) == 0:
        potential = 'null'
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not queryset.filter(**{slugfield: potential}).exists():
            return potential
        suffix += 1


def ref_uniquely(p, seq_field,  model, field='ref'):
    project = p.__class__.objects.select_for_update().get(pk=p.pk)
    ref = getattr(project, seq_field) + 1

    while True:
        params = {field: ref, 'project': project}
        if not model.objects.filter(**params).exists():
            setattr(project, seq_field, ref)
            project.save(update_fields=[seq_field])
            return ref

        time.sleep(0.0002)
        ref += 1
