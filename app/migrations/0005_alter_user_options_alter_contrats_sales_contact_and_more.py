# Generated by Django 4.0.2 on 2022-02-20 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_contrats_date_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('sales_permissions', 'sales_permissions'), ('support_permissions', 'support_permissions'))},
        ),
        migrations.AlterField(
            model_name='contrats',
            name='sales_contact',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='events',
            name='client_associe',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.clients'),
        ),
        migrations.AlterField(
            model_name='events',
            name='date_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
