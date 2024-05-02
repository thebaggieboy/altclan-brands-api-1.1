from django.contrib import admin
from .models import Merchandise
from reviews.models import Reviews
from accounts.models import BrandProfile

class BrandProfileInline(admin.TabularInline):
    model = BrandProfile
    extra = 3


class BrandProfileAdmin(admin.ModelAdmin):
    #inlines = [BrandInline]
    list_display = ['id', 'user', 'date_created',]
    list_filter = ['date_created']


class MerchandiseAdmin(admin.ModelAdmin):
    #inlines = [BrandInline]
    list_display = ['brand_name', 'merchandise_name', 'merchandise_color', 'available_sizes', 'available_colors', 'display_image', 'labels',  'price', 'delivery_cost', 'slug']
    list_filter = ['date_created']



admin.site.register(BrandProfile, BrandProfileAdmin)
admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(Reviews)




