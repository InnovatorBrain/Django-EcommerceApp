# Generated by Django 4.2.5 on 2023-09-09 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_orderitem_product_reviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]