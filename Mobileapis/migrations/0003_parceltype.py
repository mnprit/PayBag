# Generated by Django 2.2 on 2019-05-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Mobileapis', '0002_delete_contactmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
