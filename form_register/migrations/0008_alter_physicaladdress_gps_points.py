# Generated by Django 5.0.6 on 2024-08-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_register', '0007_rename_other_female_employeecategory_consultants_female_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicaladdress',
            name='GPS_Points',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
