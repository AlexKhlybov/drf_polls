# Generated by Django 2.2.10 on 2021-09-19 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_auto_20210919_1935"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answertracker",
            name="choice_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.Choice",
                verbose_name="Ответ",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_type",
            field=models.CharField(
                choices=[
                    ("Текст", "Текст"),
                    ("Одиночный выбор", "Одиночный выбор"),
                    ("Множественный выбор", "Множественный выбор"),
                ],
                default="Одиночный выбор",
                max_length=128,
                verbose_name="Тип вопроса",
            ),
        ),
    ]
