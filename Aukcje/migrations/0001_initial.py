# Generated by Django 2.0 on 2018-01-19 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aukcja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('zdjecie', models.ImageField(default='img/no-image.png', null=True, upload_to='img')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategoria', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PodKategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podkategoria', models.CharField(max_length=200)),
                ('kategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aukcje.Kategoria')),
            ],
        ),
        migrations.AddField(
            model_name='aukcja',
            name='kategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aukcje.Kategoria'),
        ),
        migrations.AddField(
            model_name='aukcja',
            name='podkategoria',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='kategoria', chained_model_field='kategoria', on_delete=django.db.models.deletion.CASCADE, to='Aukcje.PodKategoria'),
        ),
    ]
