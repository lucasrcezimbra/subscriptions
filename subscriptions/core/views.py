from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from import_export import resources
from pysympla import Sympla

from subscriptions.core.models import Subscription
from subscriptions.core.forms import ExportForm


@staff_member_required
def export(request):
    if request.method == 'GET':
        return render(request, 'export.html', {'form': ExportForm()})
    elif request.method == 'POST':
        form = ExportForm(request.POST)

        if not form.is_valid():
            return render(request, 'export.html', {'form': form})

        return _file_export_response(form.data.get('format'),
                                     form.data.getlist('fields'))


def _file_export_response(format, fields):
    subscription_resource = SubscriptionResource(fields)
    content_disposition = "attachment; filename*=utf-8''{}"
    response = HttpResponse()
    headers = {
        'csv': {
            'Content-Type': 'text/csv',
            'Content-Disposition': content_disposition.format('export.csv'),
        },
        'xlsx': {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': content_disposition.format('export.xlsx')
        },
    }

    file = getattr(subscription_resource.export(), 'get_{}'.format(format))()
    response.content = file
    for key, value in headers[format].items():
        response[key] = value

    return response


def SubscriptionResource(include_fields=[], *args, **kwargs):
    class SubscriptionResource(resources.ModelResource):
        class Meta:
            model = Subscription
            fields = include_fields

        def __init__(self):
            super(SubscriptionResource, self).__init__(*args, **kwargs)

    return SubscriptionResource()


@staff_member_required
def count_shirt_sizes(request):
    context = __get_subscription_counter_context('shirt_size')
    return render(request, 'count.html', context)


@staff_member_required
def count_subscriptions(request):
    sympla = Sympla(settings.SYMPLA_USER, settings.SYMPLA_PASSWORD)
    event = sympla.get_event(settings.SYMPLA_EVENT_ID)

    extra = {
        'sympla confirmados': int(event.confirmed_participants),
        'sympla pendentes': int(event.pending_participants),
    }
    context = __get_subscription_counter_context(
        count='import_t',
        value='import_t__origin',
        queryset=Subscription.objects.filter(import_t__gt=0),
        alone=Subscription.objects.filter(import_t__exact=None).count(),
        extra=extra,
    )
    return render(request, 'count.html', context)


@staff_member_required
def count_modality(request):
    context = __get_subscription_counter_context('modality')
    return render(request, 'count.html', context)


def __get_subscription_counter_context(count, value='', alone=0, extra={}, queryset=Subscription.objects):
    value = value if value else count
    counter = queryset.values_list(value).annotate(count=Count(count))
    extra_total = sum(extra.values())
    total = sum([count for _, count in counter]) + alone + extra_total
    return {
        'counter': counter,
        'alone': alone,
        'total': total,
        'extra': extra,
    }
