# Generated by Django 5.0.6 on 2024-07-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='num_rat',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
    ]
