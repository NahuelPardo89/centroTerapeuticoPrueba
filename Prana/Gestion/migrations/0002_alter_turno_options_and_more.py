# Generated by Django 4.1.7 on 2023-03-16 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'ordering': ['fecha', 'hora']},
        ),
        migrations.AlterField(
            model_name='precioconsulta',
            name='fecha_vigencia',
            field=models.DateField(),
        ),
    ]