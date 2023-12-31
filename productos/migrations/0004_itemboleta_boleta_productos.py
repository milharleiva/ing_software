# Generated by Django 4.2.5 on 2023-11-15 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemBoleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('boleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.boleta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
        migrations.AddField(
            model_name='boleta',
            name='productos',
            field=models.ManyToManyField(through='productos.ItemBoleta', to='productos.producto'),
        ),
    ]
