__author__ = 'anurag'

from designer.services.utils import PAGE_SIZE


def get_query_param(data):
    size = data.get('size', 60)
    page = data.get('page', 1)
    start = (page - 1) * size
    end = start + size
    return start, end, size

def get_queryset(queryset, start, end):
    total = queryset.count()
    if total - 1 > end:
        return queryset.order_by('-modified').all()[start : end], total
    else:
        return queryset.order_by('-modified').all()[start:], total


class BaseExtractor(object):

    @classmethod
    def get_by_slug(cls, model_class, slug):
        full_slug = '/%s/%s' % (model_class.__name__.lower(), slug)
        print(full_slug)
        return model_class.objects(slug__iexact=str(full_slug)).first()

    @classmethod
    def get_all(cls, queryset, **kwargs):
        start, end, size = get_query_param(kwargs)
        data, total = get_queryset(queryset, start, end)
        return data, total / size + 1
