from django.contrib import admin

from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'avatar', 'gender')
    list_filter = ('login', 'email', 'avatar', 'gender')
    search_fields = ('login', 'email', 'gender')
    readonly_fields = ('id', 'date_joined')

    fieldsets = (
        ('', {
            'fields': ('login', 'email', 'avatar', 'gender', 'first_name', 'last_name', 'phone', 'user_info')
        }),
    )


admin.site.register(Account, AccountAdmin)
