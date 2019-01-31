# Generated by Django 2.1.1 on 2018-10-26 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('points', models.IntegerField(default=0)),
                ('placement', models.IntegerField(default=0)),
                ('marbar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.MarBar')),
            ],
        ),
    ]