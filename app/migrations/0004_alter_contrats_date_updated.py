# Generated by Django 4.0.2 on 2022-02-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_contacts_contrats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrats',
            name='date_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]