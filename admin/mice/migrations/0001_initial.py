# Generated by Django 2.2.9 on 2020-02-14 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('cameras', '0001_initial'),
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('virus', models.CharField(max_length=512, null=True)),
                ('date_virus', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('Create', 'create'), ('Start', 'start'), ('Pause', 'pause'), ('Continue', 'continue'), ('Complete', 'complete')], default='create', max_length=124)),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cameras.Cameras')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'unique_together': {('experiment', 'name'), ('camera', 'experiment'), ('user', 'camera')},
            },
        ),
        migrations.CreateModel(
            name='MiceLastImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.BinaryField()),
                ('mouse', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mice.Mice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MiceImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.BinaryField()),
                ('mouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mice.Mice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MouseSimilarMouseRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouse', to='mice.Mice')),
                ('similar_mouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_mouse', to='mice.Mice')),
            ],
            options={
                'unique_together': {('mouse', 'similar_mouse')},
            },
        ),
    ]
