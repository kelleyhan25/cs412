# Generated by Django 5.1.5 on 2025-04-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0003_alter_voter_dob_alter_voter_dor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="zip_code",
            field=models.TextField(),
        ),
    ]
