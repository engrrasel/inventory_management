from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Inventory Management System")
admin.site.site_title = _("Inventory Admin")
admin.site.index_title = _("Welcome to Inventory Dashboard")
