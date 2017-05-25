from django.contrib import admin
from subscriptions.core.models import Column,Import,Subscription

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'date_of_birth','city', 'team', 'shirt_size', 'modality', 'import_')

    def import_(self, obj):
        return obj.import_t
    import_.short_description = 'Import ID'

class ImportModelAdmin(admin.ModelAdmin):
    list_display = ('pk','origin',)

class ColumnModelAdmin(admin.ModelAdmin):
    list_display = ('column_name', 'id',)

admin.site.register(Column, ColumnModelAdmin)
admin.site.register(Import, ImportModelAdmin)
admin.site.register(Subscription, SubscriptionModelAdmin)
