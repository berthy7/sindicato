# Generated by Django 4.1.1 on 2023-02-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0014_persona_fkusuariocreacion_alter_persona_fkusuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personatransferencia',
            name='fkpersonaTrans',
            field=models.IntegerField(null=True),
        ),
    ]
