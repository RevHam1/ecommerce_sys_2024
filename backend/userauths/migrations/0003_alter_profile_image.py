# Generated by Django 4.2.7 on 2024-10-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default/default-user.jpg', null=True, upload_to='image'),
        ),
    ]