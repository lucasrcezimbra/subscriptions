from django.contrib import admin
from subscriptions.core.models import Import,Subscription

admin.site.register(Subscription)
admin.site.register(Import)
