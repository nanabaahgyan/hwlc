from django.contrib import admin
from django.conf import settings

from .models import Savings, Withdrawal, Investment

# Register your models here.


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ['narration', 'member', 'amount',  'type', 'created']
    list_per_page = settings.PAGINATION_COUNT
    fields = ['narration', 'amount', ('member', 'type'), 'created']
    list_filter = ['type', 'created', 'member']
    search_fields = ['member', 'narration']
    prepopulated_fields = {'narration': ('member',)}
    raw_id_fields = ['member']
    date_hierarchy = 'created'
    ordering = ['type', 'created']


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['narration', 'amount', 'member', 'type', 'withdrawn']
    list_per_page = settings.PAGINATION_COUNT
    fields = ['narration', 'amount', ('member', 'type'),  'withdrawn']
    list_filter = ['type', 'withdrawn', 'member']
    search_fields = ['member', 'narration']
    prepopulated_fields = {'narration': ('member',)}
    raw_id_fields = ['member']
    date_hierarchy = 'withdrawn'
    ordering = ['type', 'withdrawn']


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    fields = [('narration', 'trader'), 'is_active',
              ('amount', 'rate'),
              'maturity',
              'created', 'ended', 'interest', 'members',]
    list_per_page = settings.PAGINATION_COUNT
    # raw_id_fields = ['members']
    date_hierarchy = 'created'
    list_filter = ['rate', 'amount']
    show_facets = admin.ShowFacets.ALWAYS  # type: ignore
