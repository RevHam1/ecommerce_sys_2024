# Generated by Django 4.2.7 on 2024-10-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Shop Name', max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, help_text='Shop Mobile Number', max_length=100, null=True)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=500, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
                'ordering': ['-date'],
            },
        ),
    ]