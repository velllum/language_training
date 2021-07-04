from . import models


class WordMixin:
    """- Переопределяет контекст"""
    model = models.Word
    allow_empty = False

    def get_mixin_context(self, **kwargs):
        return kwargs




