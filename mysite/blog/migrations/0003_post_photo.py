# Generated by Django 5.0 on 2024-12-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_author_post_date_created_post_date_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='post_photos/'),
        ),
    ]
