# Generated by Django 4.0.3 on 2023-02-08 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equip_app', '0004_rename_organization_id_equipment_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='serial',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]