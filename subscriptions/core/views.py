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
        subscription_resource = SubscriptionResource(form.data.getlist('fields'))
        response = HttpResponse()
        content_disposition = "attachment; filename*=utf-8''{}"
        if form.data.get('format') == 'xlsx':
            file = subscription_resource.export().get_xlsx()
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            content_disposition = content_disposition.format('export.xlsx')
        else:
            file = subscription_resource.export().csv
            response = HttpResponse(content=file)
            content_type = 'text/csv'
            content_disposition = content_disposition.format('export.csv')
        response.content = file
        response['Content-Type'] = content_type
        response['Content-Disposition'] = content_disposition
        return response

def SubscriptionResource(include_list=[], *args, **kwargs):
    class SubscriptionResource(resources.ModelResource):
        class Meta:
            model = Subscription
            fields = include_list

        def __init__(self):
            super(SubscriptionResource, self).__init__(*args, **kwargs)

    return SubscriptionResource()
