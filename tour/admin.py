from django.contrib import admin
from .models import Vendor, Package, Booking,Payment
from .models import TourPackage


admin.site.register(Vendor)
admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(Payment)

class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor', 'destination', 'price', 'approved']  # Display in the admin list
    list_filter = ['approved']  # Add a filter for approved/unapproved packages
    actions = ['approve_packages']  # Custom admin action to approve packages

    def approve_packages(self, request, queryset):
        queryset.update(approved=True)  # Bulk update to approve selected packages
        self.message_user(request, "Selected packages have been approved.")
    approve_packages.short_description = "Approve selected packages"

admin.site.register(TourPackage, TourPackageAdmin)