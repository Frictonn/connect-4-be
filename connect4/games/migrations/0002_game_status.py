# Generated by Django 3.1.1 on 2020-09-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('running', 'Running'), ('finished', 'Finished'), ('initialized', 'Initialized')], db_index=True, default='initialized', max_length=11),
        ),
    ]