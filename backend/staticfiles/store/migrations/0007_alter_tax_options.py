# Generated by Django 4.2.7 on 2024-11-19 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_tax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'ordering': ['country'], 'verbose_name_plural': 'Taxes'},
        ),
    ]