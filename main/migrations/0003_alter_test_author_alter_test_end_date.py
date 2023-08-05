# Generated by Django 4.2 on 2023-07-02 17:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0002_alter_test_author_alter_test_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="test",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="test",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 7, 12, 17, 9, 57, 7653, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
