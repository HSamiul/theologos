# Generated by Django 4.1.7 on 2023-03-15 01:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0002_alter_book_original_lang_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Translation',
        ),
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.RemoveField(
            model_name='book',
            name='original_lang_id',
        ),
        migrations.RemoveField(
            model_name='verse',
            name='original_lang_id',
        ),
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.IntegerField(default='01', primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='original_title',
            field=models.CharField(choices=[('gen', 'Genesis'), ('ex', 'Exodus'), ('lev', 'Leviticus'), ('phil', 'Philippians')], max_length=7),
        ),
        migrations.AlterField(
            model_name='book',
            name='testament',
            field=models.CharField(choices=[('old', 'Old Testament'), ('new', 'New Testament')], max_length=3),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='number',
            field=models.IntegerField(validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='verse',
            name='number',
            field=models.IntegerField(validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='verse',
            name='original_text',
            field=models.CharField(max_length=500),
        ),
        migrations.DeleteModel(
            name='Testament',
        ),
    ]
