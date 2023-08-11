from django.contrib import admin
from .models import Content, UserProfile, Domain, RankColor
from django.utils.translation import gettext_lazy


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "rank", "total_points")
    list_filter = (
        "rank",
        "user",
    )
    search_fields = ("user__username",)


class DomainAdmin(admin.ModelAdmin):
    list_display = (
        "domain_name",
        "ip_address",
        "domainIsSpecial",
        "domainAddedDate",
    )
    list_filter = ("domainIsSpecial",)
    search_fields = ("domain_name", "ip_address")


class ContentAdmin(admin.ModelAdmin):
    list_display = ("site_url", "user", "domain")
    list_filter = ("user",)
    search_fields = ("site_url", "content")


class RankColorAdmin(admin.ModelAdmin):
    list_display = ("get_rank_display", "color", "color_id")
    list_filter = ("rank",)


admin.site.site_header = gettext_lazy("Zone ")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(RankColor, RankColorAdmin)
