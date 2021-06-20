from django.db import models

"""
User
    email
    password
    status

    word_id
    
    created_date
    updated_date
    last_visit_date
    buy_office_date
"""


class Category(models.Model):
    """- Категории"""
    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Word(models.Model):
    """- Слова, примеры"""
    translation = models.CharField(max_length=255, verbose_name="Слова")  # , help_text="указывать сумму в долларах")
    example_translate = models.CharField(max_length=255, verbose_name="Пример в тексте")

    word = models.CharField(max_length=255, verbose_name="Слова")
    example = models.CharField(max_length=255, verbose_name="Пример в тексте")
    transcript = models.CharField(max_length=255, blank=True, verbose_name="Транскрипция")

    category = models.ForeignKey(
        "Category", related_name='word', on_delete=models.CASCADE, verbose_name='Категория'
    )

    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    image = models.ImageField(upload_to=f'images', blank=True, verbose_name='Изображение',)
    links_image = models.CharField(max_length=255,  blank=True, verbose_name="Ссылка на ресурс картинки")

    is_free = models.BooleanField(default=False, verbose_name='Бесплатно')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.translation

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['category']


class Services(models.Model):
    """- Услуги"""
    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    category = models.ForeignKey(
        "Category", related_name='services', on_delete=models.CASCADE, verbose_name='Категория'
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['category']

