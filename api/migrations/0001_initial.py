# Generated by Django 3.2.20 on 2023-08-23 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('price', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=25)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
    ]
