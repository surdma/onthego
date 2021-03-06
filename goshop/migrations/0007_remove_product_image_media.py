# Generated by Django 4.0.4 on 2022-05-29 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goshop', '0006_remove_category_csv_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Featured Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goshop.product', verbose_name='Product Parent')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Medias',
            },
        ),
    ]
