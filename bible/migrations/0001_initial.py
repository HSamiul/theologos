# Generated by Django 4.1.7 on 2023-03-01 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_title', models.CharField(max_length=30)),
                ('original_lang_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.book')),
            ],
        ),
        migrations.CreateModel(
            name='Testament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_title', models.CharField(max_length=30)),
                ('original_lang_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='web', max_length=10)),
                ('language', models.CharField(default='en', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('original_text', models.CharField(max_length=200)),
                ('original_lang_id', models.CharField(max_length=10)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.chapter')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='testament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.testament'),
        ),
    ]
