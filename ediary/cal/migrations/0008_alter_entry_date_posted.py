# Generated by Django 4.2.6 on 2023-11-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0007_alter_entry_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]