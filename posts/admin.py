from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'image', 'created_at')
    list_filter = ('id', 'description', 'image', 'created_at')
    search_fields = ('description', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at',)

    fieldsets = (
        ('', {
            'fields': ('id', 'description', 'image', 'created_at', 'updated_at')
        }),
    )


admin.site.register(Post, PostAdmin)
