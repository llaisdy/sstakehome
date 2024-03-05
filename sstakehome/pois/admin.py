from django.contrib import admin
from .models import PoI

@admin.register(PoI)
class PoIAdmin(admin.ModelAdmin):
    list_display = ('internal_id', 'name', 'external_id', 'category', 'avg_rating')

    @admin.display(description='Internal ID')
    def internal_id(self, obj):
        return obj.pk

    @admin.display(description='Average rating')
    def avg_rating(self, obj):
        rs = obj.ratings
        lr = len(rs)
        if not lr:
            return 0.0
        else:
            return sum([int(i) for i in rs]) / len(rs)
