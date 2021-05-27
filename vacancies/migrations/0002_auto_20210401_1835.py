# Generated by Django 3.1.7 on 2021-04-01 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True,
                                       on_delete=django.db.models.deletion.CASCADE,
                                       to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_max',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_min',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                ),
                 ),
                ('written_username', models.CharField(max_length=50)),
                ('written_phone', phonenumber_field.modelfields.PhoneNumberField(
                    blank=True,
                    max_length=128,
                    region='RU',
                    unique=True,
                ),
                 ),
                ('written_cover_letter', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='applications',
                    to=settings.AUTH_USER_MODEL,
                ),
                 ),
                ('vacancy', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='applications',
                    to='vacancies.vacancy',
                ),
                 ),
            ],
        ),
    ]
