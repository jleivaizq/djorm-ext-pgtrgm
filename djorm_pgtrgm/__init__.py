from django.db import connection
from django.db import models
from django.db.models.fields import Field, subclassing
from django.db.models.query import QuerySet
try:
    # Django 1.7 API for custom lookups
    from django.db.models import Lookup
except ImportError:
    from django.db.models.sql.constants import QUERY_TERMS
try:
    from django.contrib.gis.db.models.lookups import gis_lookups as ALL_TERMS
except ImportError:
    from django.contrib.gis.db.models.sql.query import ALL_TERMS


db_backends_allowed = ('postgresql', 'postgis')


def get_prep_lookup(self, lookup_type, value):
    try:
        return self.get_prep_lookup_origin(lookup_type, value)
    except TypeError as e:
        if lookup_type in NEW_LOOKUP_TYPE:
            return value
        raise e


def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
    try:
        value_returned = self.get_db_prep_lookup_origin(lookup_type, value,
                                                        *args, **kwargs)
    except TypeError as e:  # Django 1.1
        if lookup_type in NEW_LOOKUP_TYPE:
            return [value]
        raise e
    if value_returned is None and lookup_type in NEW_LOOKUP_TYPE:  # Dj > 1.1
        return [value]
    return value_returned


def monkey_get_db_prep_lookup(cls):
    cls.get_db_prep_lookup_origin = cls.get_db_prep_lookup
    cls.get_db_prep_lookup = get_db_prep_lookup
    if hasattr(subclassing, 'call_with_connection_and_prepared'):  # Dj > 1.1
        setattr(cls, 'get_db_prep_lookup',
                subclassing.call_with_connection_and_prepared(cls.get_db_prep_lookup))
        for new_cls in cls.__subclasses__():
            monkey_get_db_prep_lookup(new_cls)

backend_allowed = (connection.vendor.lower() in db_backends_allowed)

if backend_allowed and 'Lookup' in locals():
    # Use Django 1.7 API for registering a new lookup
    class Similar(Lookup):
        lookup_name = 'similar'

        def as_sql(self, qn, connection):
            lhs, lhs_params = self.process_lhs(qn, connection)
            rhs, rhs_params = self.process_rhs(qn, connection)
            params = lhs_params + rhs_params
            return '%s %%%% %s' % (lhs, rhs), params
    Field.register_lookup(Similar)
elif backend_allowed:
    # Old pre-Django 1.7 manual injection of lookup
    if isinstance(QUERY_TERMS, set):
        QUERY_TERMS.add('similar')
    else:
        QUERY_TERMS['similar'] = None

    if backend_allowed == 'postgis':
        if isinstance(ALL_TERMS, set):
            ALL_TERMS.add('similar')
        else:
            ALL_TERMS['similar'] = None

    connection.operators['similar'] = "%%%% %s"

    NEW_LOOKUP_TYPE = ('similar', )

    monkey_get_db_prep_lookup(Field)
    if hasattr(Field, 'get_prep_lookup'):
        Field.get_prep_lookup_origin = Field.get_prep_lookup
        Field.get_prep_lookup = get_prep_lookup


class SimilarQuerySet(QuerySet):

    def filter_o(self, **kwargs):
        qs = super(SimilarQuerySet, self).filter(**kwargs)
        for lookup, query in kwargs.items():
            query = query.replace('%', '%%')
            if lookup.endswith('__similar'):
                field = lookup.replace('__similar', '')
                select = {'%s_distance' % field: "similarity(%s, '%s')" % (field, query)}
                qs = qs.extra(select=select).order_by('-%s_distance' % field)
        return qs


class SimilarManager(models.Manager):

    def get_queryset(self):
        return SimilarQuerySet(self.model, using=self._db)

    def filter_o(self, **kwargs):
        return self.get_queryset().filter_o(**kwargs)
