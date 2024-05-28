from django.contrib import admin

# Register your models here.
from .models import Detail, Prop

class PropAdmin(admin.ModelAdmin):
    list_display=("id", "name", "p_type")

admin.site.register(Prop, PropAdmin)


class DetailAdmin(admin.ModelAdmin):
    list_display=('id', 'target_id', 'occur_date', 'amount')

admin.site.register(Detail, DetailAdmin)