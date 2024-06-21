# Generated by Django 5.0.6 on 2024-06-13 10:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='proposed',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='proposed',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='children',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='employer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='id_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='occupation',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='relationship_status',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='salary_range',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proposed',
            name='seconder_userid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
