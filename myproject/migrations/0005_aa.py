# Generated by Django 5.0.4 on 2024-04-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0004_delete_aa'),
    ]

    operations = [
        migrations.CreateModel(
            name='AA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
            ],
        ),
    ]
