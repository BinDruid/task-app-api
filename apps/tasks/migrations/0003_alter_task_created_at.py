# Generated by Django 5.0a1 on 2023-10-24 08:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_alter_task_created_at_alter_task_finished_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="تاریخ ایجاد"
            ),
        ),
    ]