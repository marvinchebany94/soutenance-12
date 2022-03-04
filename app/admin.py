from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Clients, Contrats, Events
# Register your models here.
admin.site.register(User)


@admin.register(Clients)
class ClientsAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'mobile',
                    'company_name', 'sales_contact')

    def get_queryset(self, request):
        qs = super(ClientsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sales_contact=request.user)


@admin.register(Contrats)
class ContratsAdmin(ModelAdmin):
    list_display = ('client_associe', 'status', 'amout', 'payement_due',
                    'sales_contact')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContratsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['sales_contact'].queryset = User.objects.filter(
            equipe='vente')
        return form
    readonly_fields = ('client_associe',)


@admin.register(Events)
class EventsAdmin(ModelAdmin):
    list_display = ('client_associe', 'participants', 'event_date', 'notes',
                    'support_contact')

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['support_contact'].queryset = User.objects.filter(
            equipe='gestion')
        return form
    readonly_fields = ('client_associe',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return self.readonly_fields