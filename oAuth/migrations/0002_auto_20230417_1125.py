# Generated by Django 3.2.9 on 2023-04-17 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oAuth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fintime',
        ),
        migrations.AddField(
            model_name='user',
            name='fin_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fin_time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='business_activate',
            field=models.IntegerField(choices=[[0, 'deactivated'], [1, 'activated']], default=0, verbose_name='B_Activated'),
        ),
    ]