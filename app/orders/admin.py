from django.contrib import admin

from .models import Product, Category, Order

from django.contrib.admin.views.main import ChangeList
from .forms import OrderChangeListForm


class OrderChangeList(ChangeList):

    def __init__(self, request, model, list_display,
                 list_display_links, list_filter, date_hierarchy,
                 search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin, sortable_by):
        super(OrderChangeList, self).__init__(request, model,
                                              list_display, list_display_links, list_filter,
                                              date_hierarchy, search_fields, list_select_related,
                                              list_per_page, list_max_show_all, list_editable,
                                              model_admin, sortable_by)

        self.list_display = ['action_checkbox', 'price', 'products']
        self.list_display_links = ['price']
        self.list_editable = ['products']


class OrderAdmin(admin.ModelAdmin):

    def get_changelist(self, request, **kwargs):
        return OrderChangeList

    def get_changelist_form(self, request, **kwargs):
        return OrderChangeListForm


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
