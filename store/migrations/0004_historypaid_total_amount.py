# Generated by Django 4.1 on 2023-03-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_historypaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='historypaid',
            name='total_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]