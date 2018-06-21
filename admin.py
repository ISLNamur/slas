from django.contrib import admin

from .models import Activity, ActivityInscription


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'slot', 'animator')

admin.site.register(Activity, ActivityAdmin)


class ActivityInscriptionAdmin(admin.ModelAdmin):
    list_display = ('activity', 'student_first_name', 'student_surname', 'datetime_inscription')

admin.site.register(ActivityInscription, ActivityInscriptionAdmin)
