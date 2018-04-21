# Generated by Django 2.0.4 on 2018-04-21 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0003_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='payment_style',
            field=models.CharField(choices=[('CARD', 'Credit Card'), ('COD', 'Cash on Delivery')], default='COD', max_length=100),
        ),
    ]
