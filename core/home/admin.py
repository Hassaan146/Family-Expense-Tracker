from django.contrib import admin
from .models import Family, User_a , Expenses
# Register your models here.
class Familymemberdisplay(admin.ModelAdmin):
    list_display = ['member_name','member_age','member_gender']
admin.site.register(Family,Familymemberdisplay)
admin.site.register(User_a)
admin.site.register(Expenses)
