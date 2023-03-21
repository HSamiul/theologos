# Generated by Django 4.1.7 on 2023-03-21 02:20

import django.core.validators
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
                ('number', models.IntegerField(default='01', primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(2)])),
                ('original_title', models.CharField(choices=[('gen', 'Genesis'), ('ex', 'Exodus'), ('lev', 'Leviticus'), ('phil', 'Philippians')], max_length=7)),
                ('testament', models.CharField(choices=[('old', 'Old Testament'), ('new', 'New Testament')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.book')),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)])),
                ('original_text', models.CharField(max_length=500)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.chapter')),
            ],
        ),
    ]
