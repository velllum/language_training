from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ("id", "name", "slug", "updated_date", "created_date", )
    list_display_links = ("name",)


@admin.register(models.Services)
class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ("id", "name", "category", "price", "slug", "updated_date", "created_date",)
    list_display_links = ("id",)
    search_fields = ("name", "category__name",)
    list_filter = ("category",)
    save_as = True
    list_editable = ("name", "category", "price", "slug")


@admin.register(models.Word)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('translation',)}
    list_display = (
        "id", "translation", "word", "transcript", "category",
        "image", "links_image", "is_free", "is_published", "slug",
        "updated_date", "created_date",
    )
    list_display_links = ("id",)
    search_fields = (
        "translation", "word", "transcript",
    )
    list_filter = ("category", "is_published", "is_free",)
    save_as = True
    list_editable = (
        "translation", "word", "transcript", "category",
        "image", "links_image", "is_free", "is_published", "slug",
    )
    fieldsets = (
        ("Слова на иностранном", {
            "fields": ("word", "example", "transcript")
        }),
        ("Перевод на русском", {
            "fields": ("translation", "example_translate",  "slug")
        }),
        ("Картинка", {
            "fields": ("image", "links_image")
        }),
        ("Статус", {
            "fields": ("is_free", "is_published")
        }),
    )


admin.site.site_title = "Админ панель"
admin.site.site_header = "Админ панель"
