from django.contrib import admin

# Register your models here.
from .models import DATT

@admin.register(DATT)
class DATTAdmin(admin.ModelAdmin):
    list_display = ("room", "CO", "HUM", "TEMP",)
    search_fields = ("room",)