# Generated by Django 1.11.16 on 2018-11-30 08:54
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('post_office', '0007_auto_20170731_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='headers',
            field=models.JSONField(blank=True, null=True, verbose_name='Headers'),
        ),
    ]
