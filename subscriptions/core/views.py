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

        return file_export_response(form.data.get('format'),
                                    form.data.getlist('fields'))

def file_export_response(format, fields):
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
