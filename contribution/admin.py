from django.contrib import admin

from .models import Savings, Withdrawal, PensionSavings

# Register your models here.


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ['narration', 'member', 'amount',  'type', 'created']
    fields = ['narration', 'amount', ('member', 'type'), 'created']
    list_filter = ['type', 'created', 'member']
    search_fields = ['member', 'narration']
    prepopulated_fields = {'narration': ('member',)}
    raw_id_fields = ['member']
    date_hierarchy = 'created'
    ordering = ['type', 'created']


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['narration', 'amount', 'member', 'type', 'when']
    fields = ['narration', 'amount', ('member', 'type'),  'when']
    list_filter = ['type', 'when', 'member']
    search_fields = ['member', 'narration']
    prepopulated_fields = {'narration': ('member',)}
    raw_id_fields = ['member']
    date_hierarchy = 'when'
    ordering = ['type', 'when']
