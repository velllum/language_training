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
    """Категории"""
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='Url')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Word(models.Model):
    """Слова, примеры"""
    word = models.CharField(max_length=255, verbose_name="Слова")
    example = models.CharField(max_length=255, verbose_name="Пример в тексте")
    transcript = models.CharField(max_length=255, verbose_name="Транскрипция")

    category = models.ForeignKey(
        "Category", verbose_name='Категория', related_name='word', on_delete=models.CASCADE
    )

    translation = models.CharField(max_length=255, verbose_name="Перевод слова")
    example_translate = models.CharField(max_length=255, verbose_name="Пример перевода в тексте")

    slug = models.SlugField(unique=True, verbose_name='Url')
    image = models.ImageField(upload_to='media/', verbose_name='Изображение', blank=True)
    links_image = models.CharField(max_length=255, verbose_name="Ссылка на ресурс картинки")

    is_free = models.BooleanField(default=False, verbose_name='Статус бесплатно')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.translation} - {self.example_translate}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['category']


class Services(models.Model):
    """Услуги"""
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='Url')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    category = models.ForeignKey(
        "Category", verbose_name='Категория', related_name='services', on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['category']

