# Generated by Django 4.0.3 on 2023-01-27 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equip_app', '0003_rename_organization_equipment_organization_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='organization_id',
            new_name='organization',
        ),
    ]
