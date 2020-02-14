# Generated by Django 2.2.9 on 2020-02-14 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('status', models.CharField(choices=[('Create', 'create'), ('Start', 'start'), ('Pause', 'pause'), ('Continue', 'continue'), ('Complete', 'complete')], default='create', max_length=124)),
                ('place', models.CharField(max_length=512, null=True)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'unique_together': {('user', 'title')},
            },
        ),
    ]
