from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey


def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class Kategoria(models.Model):
    kategoria = models.CharField(max_length=200)
    def __str__(self):
        return self.kategoria

class PodKategoria(models.Model):
    kategoria = models.ForeignKey('Kategoria', on_delete=models.CASCADE)
    podkategoria = models.CharField(max_length=200)

    def __str__(self):
        return self.podkategoria


class Aukcja(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(
            blank=True, null=True)
    kategoria = models.ForeignKey('Kategoria', on_delete=models.CASCADE, null=False)
    podkategoria = ChainedForeignKey(
        'PodKategoria',
        chained_field="kategoria",
        chained_model_field="kategoria",
        show_all=False,
        auto_choose=True,
        sort=True,
        )
    zdjecie = models.ImageField(upload_to = 'img',default='img/no-image.png', null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Komentarz(models.Model):
    autor = models.ForeignKey('auth.User',related_name='autor', on_delete=models.CASCADE)
    komentowany = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE)
    text = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    zatwierdzony = models.BooleanField(default=False)

    def zatwierdz(self):
        self.zatwierdzony = True
        self.save()

    def __str__(self):
        return self.text