# Generated by Django 5.2.1 on 2025-05-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admindash', '0002_delete_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(default='Inactive', max_length=20),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
