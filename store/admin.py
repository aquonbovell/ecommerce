from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Product, Customer, Order, Profile


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(Order)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profiles"


class UserAdmin(admin.ModelAdmin):
    fields = ["username", "email", "first_name", "last_name"]
    inlines = (ProfileInline,)
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    ordering = ["username"]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
