# Generated by Django 3.2.9 on 2023-05-16 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oAuth', '0010_oauthtestdata'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='oauthtestdata',
            index_together={('code', 'date')},
        ),
    ]