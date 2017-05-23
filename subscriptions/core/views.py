from django.shortcuts import render
from subscriptions.core.forms import SubscriptionForm

def get_import(request):
    return render(request, 'import.html', {'form': SubscriptionForm()})
