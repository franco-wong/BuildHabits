# Generated by Django 2.2.7 on 2019-11-25 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuildHabits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habit_text', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(verbose_name='date added')),
                ('occurrence', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TodayHabitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_date', models.DateTimeField(verbose_name='date habit is performed')),
                ('completed', models.BooleanField(default=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuildHabits.Habit')),
            ],
        ),
        migrations.DeleteModel(
            name='Habits',
        ),
    ]
