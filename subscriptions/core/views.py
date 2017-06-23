from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from import_export import resources
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
def shirt_sizes(request):
    shirt_sizes = Subscription.objects.values('shirt_size')\
                    .annotate(count=Count('shirt_size'))
    return render(request, 'shirt_sizes.html', {'shirt_sizes': shirt_sizes})

@staff_member_required
def count_subscriptions(request):
    imports_count = Subscription.objects\
                        .filter(import_t__gt=0)\
                        .values('import_t__origin')\
                        .annotate(count=Count('import_t'))
    without_imports_count = Subscription.objects\
                                .filter(import_t__exact=None)\
                                .count()
    total = sum([ic['count'] for ic in imports_count]) + without_imports_count
    context = {
        'imports_count': imports_count,
        'without_imports_count': without_imports_count,
        'total': total
    }
    return render(request, 'count_imports.html', context)

@staff_member_required
def count_modalities(request):
    modalities_count = Subscription.objects.values('modality')\
                    .annotate(count=Count('modality'))
    total = Subscription.objects.count()
    context = {
        'modalities': modalities_count,
        'total': total,
    }
    return render(request, 'count_modalities.html', context)
