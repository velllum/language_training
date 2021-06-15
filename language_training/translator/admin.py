from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models
from . import resources


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
    search_fields = ("category__name",)
    list_filter = ("category",)
    save_as = True
    list_editable = ("category", "name", "price", "slug")


@admin.register(models.Word)
class WordAdmin(ImportExportModelAdmin):
    list_per_page = 30
    prepopulated_fields = {'slug': ('category', 'translation',)}
    list_display = (
        "id", "category", "translation", "word", "transcript",
        "image", "links_image",  "slug", "is_free", "is_published",
        "updated_date", "created_date",
    )
    list_display_links = ("id",)
    search_fields = (
        "translation", "word", "transcript",
    )
    list_filter = ("category", "is_published", "is_free",)
    resource_class = resources.WordResource
    save_as = True
    list_editable = (
        "category", "translation", "word", "transcript",
        "is_free", "is_published", "slug",
    )
    fieldsets = (
        ("Выбор категории", {
            "fields": ("category",)
        }),
        ("Русском перевод", {
            "fields": ("translation", "example_translate", "slug")
        }),
        ("Иностранный перевод", {
            "fields": ("word", "example", "transcript")
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
