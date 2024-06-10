from django.contrib import admin
from .models import ShippingAddress, Order, OrderItems

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)


# Create orderItem Inline
class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]
    readonly_fields = ("date_ordered",)


admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)
