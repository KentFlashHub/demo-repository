# Generated by Django 4.2.11 on 2024-04-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_auto_20200902_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
