from django.contrib import admin
from django.forms import TextInput
from django.utils.safestring import mark_safe
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
    formfield_overrides = {
        models.models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    list_per_page = 30
    prepopulated_fields = {'slug': ('category', 'word',)}
    list_display = (
        "id", "category", "translation", "word", "transcript",
        "slug", "is_free", "is_published",
        "updated_date", "created_date",
    )
    list_display_links = ("id",)
    search_fields = (
        "translation", "word", "transcript"
    )
    list_filter = ("category", "is_published", "is_free",)
    resource_class = resources.WordResource
    save_as = True
    list_editable = (
        "translation", "word", "transcript",
        "is_free", "is_published", "slug",
    )
    readonly_fields = ("get_html_photo", )
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
            "fields": ("image", "get_html_photo", "links_image")
        }),
        ("Статус", {
            "fields": ("is_free", "is_published")
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """- Меняет размеры указанных полей формы"""
        form = super(WordAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['example_translate'].widget.attrs['style'] = 'width: 45em;'
        form.base_fields['example'].widget.attrs['style'] = 'width: 45em;'
        return form

    def get_html_photo(self, obj):
        """- Добавляет картинку к слову"""
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")
        return mark_safe("<img src='/media/images/placeholder.png' width=50>")

    get_html_photo.short_description = "Миниатюра"


admin.site.site_title = "Админ панель"
admin.site.site_header = "Админ панель"
