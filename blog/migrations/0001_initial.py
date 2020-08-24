# Generated by Django 3.0.8 on 2020-08-14 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('header', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('sub_header', models.CharField(max_length=200, null=True)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_date', models.DateTimeField()),
                ('content', models.CharField(max_length=5000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment')),
            ],
        ),
    ]
