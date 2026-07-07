from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'time', 'venue', 'capacity', 'ticket_price', 'status')
    list_filter = ('status', 'category', 'date')
    search_fields = ('title', 'venue', 'description')
    ordering = ('date', 'time')
    date_hierarchy = 'date'
