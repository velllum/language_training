from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("id", "title", "slug")
    list_display_links = ("title",)


@admin.register(models.Services)
class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("id", "title", "category", "price", "slug")
    list_display_links = ("title",)
    search_fields = ("title", "category__title",)
    list_filter = ("category",)
    save_as = True


@admin.register(models.Word)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("id", "title", "services", "slug", "is_published")
    list_display_links = ("title",)
    search_fields = ("title", "services__title")
    list_filter = ("title", "services", "is_published")
    save_as = True
    list_editable = ("is_published",)
    fieldsets = (
        ("SEO поля", {
            "fields": (("keywords", "meta_title", "description"),)
        }),
        ("Контент", {
            "fields": (("services",), ("title", "slug"), "content", "image", "is_published")
        })
    )


admin.site.site_title = "Админ панель"
admin.site.site_header = "Админ панель"
