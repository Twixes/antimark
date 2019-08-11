# Generated by Django 2.2.4 on 2019-08-11 02:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Completion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
            ],
            options={
                'verbose_name': 'completion',
                'verbose_name_plural': 'completions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(default=1, unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='position')),
                ('text', models.CharField(max_length=100, unique=True, verbose_name='text')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('MR', 'Mr.'), ('MS', 'Ms.')], max_length=10, verbose_name='title')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='mark')),
                ('completion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', related_query_name='vote', to='poll.Completion', verbose_name='question')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', related_query_name='vote', to='poll.Question', verbose_name='question')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', related_query_name='vote', to='poll.Teacher', verbose_name='teacher')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('name_teacher_selection_case', models.CharField(max_length=50, null=True, verbose_name='name in "Who teaches you …?" case (e.g. "English")')),
                ('teachers', models.ManyToManyField(related_name='subjects', related_query_name='subject', to='poll.Teacher', verbose_name='teachers')),
            ],
            options={
                'verbose_name': 'subject',
                'verbose_name_plural': 'subjects',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('number_of_students', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='number of students')),
                ('subjects', models.ManyToManyField(related_name='groups', related_query_name='group', to='poll.Subject', verbose_name='subjects')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='completion',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', related_query_name='vote', to='poll.Group', verbose_name='group'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='poll.Group', verbose_name='group')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='poll.Subject', verbose_name='subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='poll.Teacher', verbose_name='teacher')),
            ],
            options={
                'verbose_name': 'assignment',
                'verbose_name_plural': 'assignments',
            },
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('completion', 'question', 'teacher'), name='unique_vote'),
        ),
        migrations.AddConstraint(
            model_name='assignment',
            constraint=models.UniqueConstraint(fields=('group', 'subject', 'teacher'), name='unique_assignment'),
        ),
    ]
