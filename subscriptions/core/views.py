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
        file = SubscriptionResource(form.data.getlist('fields')).export().csv
        response = HttpResponse(content=file)
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}"\
                                           .format('export.csv')
        return response


def SubscriptionResource(include_list=[], *args, **kwargs):
    class SubscriptionResource(resources.ModelResource):
        class Meta:
            model = Subscription
            fields = include_list

        def __init__(self):
            super(SubscriptionResource, self).__init__(*args, **kwargs)

    return SubscriptionResource()
