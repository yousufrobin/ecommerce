# Generated by Django 4.0.5 on 2022-11-29 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.product'),
        ),
    ]
