# Generated by Django 3.2.9 on 2023-06-11 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oAuth', '0045_oauthstockdata20204_oauthstockdata20211_oauthstockdata20212_oauthstockdata20213_oauthstockdata20214_'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OauthStockData20232',
            new_name='OauthStockData2023_1',
        ),
        migrations.RenameModel(
            old_name='OauthStockData20231',
            new_name='OauthStockData2023_2',
        ),
        migrations.AlterModelTable(
            name='oauthstockdata2023_1',
            table='oauth_stockdata20231',
        ),
        migrations.AlterModelTable(
            name='oauthstockdata2023_2',
            table='oauth_stockdata20232',
        ),
    ]