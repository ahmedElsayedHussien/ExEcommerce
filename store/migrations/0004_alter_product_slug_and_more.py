# Generated by Django 4.2.7 on 2024-12-01 22:46

from django.db import migrations, models
from django.utils.text import slugify

def make_slugs_unique(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for product in Product.objects.all():
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        if product.slug != slug:
            product.slug = slug
            product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_user'),
    ]

    operations = [
        migrations.RunPython(make_slugs_unique),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['slug'], name='store_produ_slug_361302_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='store_produ_name_5e57da_idx'),
        ),
    ]
