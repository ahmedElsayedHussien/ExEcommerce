# Generated by Django 4.2.7 on 2024-12-02 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_cartitem_discount_percent_at_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, help_text='Recommended size: 200x200 pixels', null=True, upload_to='categories/'),
        ),
    ]
