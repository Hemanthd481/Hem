from django.contrib import admin
from .models import RoomAssignment


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room_number', 'created_at')