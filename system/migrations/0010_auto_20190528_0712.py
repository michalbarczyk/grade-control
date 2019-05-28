# Generated by Django 2.2 on 2019-05-28 07:12

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_auto_20190509_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('2.0', 'chlip'), ('3.0', 'ok'), ('3.5', 'ok +'), ('4.0', 'dobre'), ('4.5', 'dobre +'), ('5.0', 'bardzodobre')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='PercentGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='ScoreGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='grade_type',
            field=models.CharField(choices=[('academic_grade', 'academic grade'), ('score_grade', 'score grade'), ('percent_grade', 'percent grade')], default='academic_grade', max_length=64),
        ),
        migrations.AddField(
            model_name='event',
            name='max_score',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='event',
            name='weight',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 28, 7, 12, 17, 340950)),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.AddField(
            model_name='scoregrade',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Event'),
        ),
        migrations.AddField(
            model_name='scoregrade',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Student'),
        ),
        migrations.AddField(
            model_name='percentgrade',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Event'),
        ),
        migrations.AddField(
            model_name='percentgrade',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Student'),
        ),
        migrations.AddField(
            model_name='academicgrade',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Event'),
        ),
        migrations.AddField(
            model_name='academicgrade',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='scoregrade',
            unique_together={('owner', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='percentgrade',
            unique_together={('owner', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='academicgrade',
            unique_together={('owner', 'event')},
        ),
    ]