# Generated by Django 3.2.4 on 2021-07-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bschedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bdate', models.CharField(max_length=8)),
                ('btime', models.CharField(max_length=5)),
                ('bday', models.CharField(max_length=3)),
                ('bbname', models.CharField(max_length=10)),
                ('bone', models.CharField(max_length=12)),
                ('btwo', models.CharField(max_length=12)),
                ('bthree', models.CharField(max_length=12)),
                ('bfour', models.CharField(max_length=12)),
                ('bfive', models.CharField(max_length=12)),
                ('bsix', models.CharField(max_length=12)),
                ('bsisdeleted', models.CharField(max_length=1)),
            ],
        ),
    ]
