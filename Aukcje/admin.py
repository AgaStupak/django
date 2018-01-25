from django.contrib import admin
from .models import Aukcja, Kategoria, PodKategoria, Komentarz

admin.site.register(Aukcja)
admin.site.register(Kategoria)
admin.site.register(PodKategoria)
admin.site.register(Komentarz)