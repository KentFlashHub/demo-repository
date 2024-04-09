

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='known',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
