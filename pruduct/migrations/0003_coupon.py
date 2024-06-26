# Generated by Django 5.0.3 on 2024-04-05 04:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pruduct', '0002_colorvariant_sizevariant_product_color_variant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('coupon_code', models.CharField(max_length=100, unique=True)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=0)),
                ('minimum_amount', models.IntegerField(default=None)),
                ('maximum_amount', models.IntegerField(default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
