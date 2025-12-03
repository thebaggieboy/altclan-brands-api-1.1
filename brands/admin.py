from django.contrib import admin
from .models import Merchandise
from reviews.models import Reviews


class MerchandiseAdmin(admin.ModelAdmin):
    #inlines = [BrandInline]
    list_display = ['brand_name', 'merchandise_name', 'merchandise_color', 'available_sizes', 'available_colors', 'display_image', 'labels',  'price', 'delivery_cost', 'slug']
    list_filter = ['date_created']


admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(Reviews)




