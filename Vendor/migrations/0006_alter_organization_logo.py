# Generated by Django 4.0.5 on 2022-06-11 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0005_orderdeatails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.TextField(),
        ),
    ]