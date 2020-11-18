from django.contrib import admin

# Register your models here.
from .models import Nash_message, Nash_messageLike


class Nash_messageLikeAdmin(admin.TabularInline):
    model = Nash_messageLike

class Nash_messageAdmin(admin.ModelAdmin):
    inlines = [Nash_messageLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Nash_message

admin.site.register(Nash_message, Nash_messageAdmin)


