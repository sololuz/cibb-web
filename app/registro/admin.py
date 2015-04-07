from django.contrib import admin
from registro.models import (
    Attend,
    Suscriptor,
    Contact,
    Speaker,
    Staff,
    Sponsor,
)


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


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", )
    search_fields = ("full_name", "organization", )


class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", )
    search_fields = ("full_name", )


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name", "logo", )
    search_fields = ("name", )

admin.site.register(Attend, AttendAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Sponsor, SponsorAdmin)
