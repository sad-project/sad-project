# Generated by Django 4.1.7 on 2023-03-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sadio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='type',
            field=models.CharField(default='generic', max_length=255),
        ),
    ]