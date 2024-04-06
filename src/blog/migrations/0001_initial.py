# Generated by Django 4.2.6 on 2024-04-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("subtitle", models.CharField(max_length=100)),
                ("body", models.TextField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
    ]