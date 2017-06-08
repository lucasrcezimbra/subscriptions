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
        return export_file_response(form.data.get('format'),
                                    form.data.getlist('fields'))

def export_file_response(format, fields):
    content_disposition = "attachment; filename*=utf-8''{}"
    FORMATS = {
        'csv': {
            'Content-Type': 'text/csv',
            'Content-Disposition': content_disposition.format('export.csv'),
        },
        'xlsx': {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': content_disposition.format('export.xlsx')
        },
    }
    subscription_resource = SubscriptionResource(fields)
    response = HttpResponse()
    if format == 'xlsx':
        response.content = subscription_resource.export().get_xlsx()
    else:
        response.content = subscription_resource.export().csv

    for key, value in FORMATS[format].items():
        response[key] = value
    return response

def SubscriptionResource(include_list=[], *args, **kwargs):
    class SubscriptionResource(resources.ModelResource):
        class Meta:
            model = Subscription
            fields = include_list

        def __init__(self):
            super(SubscriptionResource, self).__init__(*args, **kwargs)

    return SubscriptionResource()
