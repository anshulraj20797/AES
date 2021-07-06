# Generated by Django 3.2 on 2021-07-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_inventoryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyledgermaster',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='companyledgermaster',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='unit',
            field=models.CharField(choices=[('KG', 'KG'), ('METER', 'METER')], max_length=255),
        ),
        migrations.AlterField(
            model_name='transactionlineitemdetails',
            name='unit',
            field=models.CharField(choices=[('KG', 'KG'), ('METER', 'METER')], max_length=255),
        ),
    ]