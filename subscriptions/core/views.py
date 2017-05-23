from django.shortcuts import render
from subscriptions.core.forms import SubscriptionForm
from subscriptions.core.helpers import SubscriptionImporter

def get_import(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        filepath = handle_uploaded_file(request.FILES['file'])
        importer = SubscriptionImporter(filepath)
        importer.save()
        return render(request, 'import_ok.html', {'form': SubscriptionForm()})
    elif request.method == 'GET':
        return render(request, 'import.html', {'form': SubscriptionForm()})

def handle_uploaded_file(f):
    filepath = 'upload.csv'
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filepath

