# Generated by Django 4.1.1 on 2022-10-31 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_created_at_post_deleted_at_post_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(max_length=200, verbose_name='Описание'),
        ),
    ]