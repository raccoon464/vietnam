from django.contrib import admin

# Register your models here.
from .models import User
from .models import Message
from .models import Error
from .models import Admin_rule
from .models import Lang

admin.site.register(Message)
admin.site.register(Error)
admin.site.register(Lang)
admin.site.register(Admin_rule)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'name')