# Generated by Django 5.0.6 on 2024-07-08 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='option1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option4',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
