from django.contrib import admin
from registro.models import Attend, Suscriptor, Contact


class AttendAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "depot", "package", "city", )
    list_filter = ("package", "city", )
    search_fields = ("name", "surname", "depot", )


class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ("email", "date", )
    search_fields = ("email", )

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")
    search_fields = ("email", )

admin.site.register(Attend, AttendAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(Contact, ContactAdmin)
