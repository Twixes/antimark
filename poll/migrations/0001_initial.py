# Generated by Django 2.2.4 on 2019-08-14 23:28

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.SlugField(help_text='30 characters or fewer. Letters, digits, underscores and hyphens only.', max_length=30, unique=True, verbose_name='username')),
                ('school_name', models.CharField(max_length=50, verbose_name='school name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('nomenclature', models.CharField(choices=[('teachers', 'teachers'), ('professors', 'professors')], default='teachers', max_length=30, verbose_name='nomenclature')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'school',
                'verbose_name_plural': 'schools',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Completion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', related_query_name='completion', to=settings.AUTH_USER_MODEL, verbose_name='school')),
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
                ('position', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='position')),
                ('text', models.CharField(max_length=100, verbose_name='text')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', related_query_name='question', to=settings.AUTH_USER_MODEL, verbose_name='school')),
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
                ('title', models.CharField(choices=[(None, 'None'), ('MR', 'Mr.'), ('MS', 'Ms.')], max_length=10, null=True, verbose_name='title')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', related_query_name='teacher', to=settings.AUTH_USER_MODEL, verbose_name='school')),
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
                ('mark', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='mark')),
                ('completion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', related_query_name='vote', to='poll.Completion', verbose_name='completion')),
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
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('name_teacher_selection_case', models.CharField(default=None, max_length=50, null=True, verbose_name='name in "Who teaches you …?" case (e.g. "English")')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', related_query_name='subject', to=settings.AUTH_USER_MODEL, verbose_name='school')),
                ('teachers', models.ManyToManyField(related_name='subjects', related_query_name='subject', to='poll.Teacher', verbose_name='teachers')),
            ],
            options={
                'verbose_name': 'subject',
                'verbose_name_plural': 'subjects',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('number_of_students', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='number of students')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_groups', related_query_name='student_group', to=settings.AUTH_USER_MODEL, verbose_name='school')),
                ('subjects', models.ManyToManyField(related_name='student_groups', related_query_name='student_group', to='poll.Subject', verbose_name='subjects')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='completion',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', related_query_name='completion', to='poll.StudentGroup', verbose_name='group'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to=settings.AUTH_USER_MODEL, verbose_name='school')),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', related_query_name='assignment', to='poll.StudentGroup', verbose_name='group')),
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
            model_name='subject',
            constraint=models.UniqueConstraint(fields=('school', 'name'), name='unique_subject_name'),
        ),
        migrations.AddConstraint(
            model_name='studentgroup',
            constraint=models.UniqueConstraint(fields=('school', 'name'), name='unique_student_group_name'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('school', 'position'), name='unique_question_position'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('school', 'text'), name='unique_question_text'),
        ),
        migrations.AddConstraint(
            model_name='assignment',
            constraint=models.UniqueConstraint(fields=('school', 'student_group', 'subject', 'teacher'), name='unique_assignment'),
        ),
    ]
