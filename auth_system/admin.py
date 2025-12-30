from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active',
        'is_staff',
        'last_login',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
    )

    ordering = ('-date_joined',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('email',)
        }),
        ('Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'followers_count',
        'following_count',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'followers_count',
        'following_count',
        'created_at',
        'updated_at',
    )