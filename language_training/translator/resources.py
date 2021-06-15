from import_export import resources
from . import models


class WordResource(resources.ModelResource):
    class Meta:
        model = models.Word
        fields = (
            'id',
            'translation', 'example_translate',
            'word', 'example', 'transcript',
            'category',
            'slug',
        )
