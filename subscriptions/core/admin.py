from django.contrib import admin
from subscriptions.core.models import Import,Subscription

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'date_of_birth','city', 'team', 'shirt_size', 'modality', 'import_')

    def import_(self, obj):
        return obj.import_t
    import_.short_description = 'Import ID'

class ImportModelAdmin(admin.ModelAdmin):
    list_display = ('pk','origin',)

admin.site.register(Subscription, SubscriptionModelAdmin)
admin.site.register(Import, ImportModelAdmin)
