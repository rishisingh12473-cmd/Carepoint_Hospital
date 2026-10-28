from django.contrib import admin

from .models import Appointment, contactus


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "department",
        "appointment_date",
        "phone",
        "status",
        "created_at",
    )
    list_filter = ("status", "department", "appointment_date")
    search_fields = ("patient_name", "email", "phone")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    ordering = ("appointment_date",)


@admin.register(contactus)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "mobile")
    search_fields = ("name", "email", "mobile", "message")


admin.site.site_header = "CarePoint Hospital Administration"
admin.site.site_title = "CarePoint Administration"
admin.site.index_title = "Hospital management"
