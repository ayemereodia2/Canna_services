# Generated by Django 4.2.6 on 2023-11-28 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0002_alter_customuser_managers_remove_customuser_otp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
