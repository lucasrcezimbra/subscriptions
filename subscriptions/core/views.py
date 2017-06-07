from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from subscriptions.core.models import Subscription
from subscriptions.core.forms import ExportForm

@staff_member_required
def export(request):
    return render(request, 'export.html', {'form': ExportForm()})
