# Generated by Django 3.2 on 2021-05-27 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user_activity', '0006_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_date']},
        ),
        migrations.AlterField(
            model_name='like',
            name='liked_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]