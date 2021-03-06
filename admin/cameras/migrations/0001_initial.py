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
            name='Cameras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('ip', models.CharField(max_length=512)),
                ('place', models.CharField(max_length=512, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'unique_together': {('user', 'ip')},
            },
        ),
    ]
