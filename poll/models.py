from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy, pgettext_lazy


class SchoolManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, school_name: str, email: str, password: str, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not school_name:
            raise ValueError('The given school_name must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given password must be set')
        username = self.model.normalize_username(username)
        school_name = school_name.strip()
        email = self.normalize_email(email)
        user = self.model(username=username, school_name=school_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, school_name: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, school_name, email, password, **extra_fields)

    def create_superuser(self, username: str, school_name: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, school_name, email, password, **extra_fields)


class School(AbstractBaseUser, PermissionsMixin):
    TEACHERS = 'teachers'
    PROFESSORS = 'professors'
    NOMENCLATURE_CHOICES = [
        (TEACHERS, gettext_lazy('teachers')),
        (PROFESSORS, gettext_lazy('professors'))
    ]
    username = models.SlugField(
        max_length=30, unique=True, verbose_name=gettext_lazy('username'),
        help_text=gettext_lazy('30 characters or fewer. Letters, digits, underscores and hyphens only.')
    )
    school_name = models.CharField(max_length=50, verbose_name=gettext_lazy('school name'))
    email = models.EmailField(verbose_name=gettext_lazy('email address'))
    nomenclature = models.CharField(
        max_length=30, choices=NOMENCLATURE_CHOICES, default=TEACHERS, verbose_name=gettext_lazy('nomenclature')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=gettext_lazy('staff status'),
        help_text=gettext_lazy('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        default=True, verbose_name=gettext_lazy('active'),
        help_text=gettext_lazy(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=gettext_lazy('date joined'))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['school_name', 'email']

    class Meta:
        verbose_name = gettext_lazy('school')
        verbose_name_plural = gettext_lazy('schools')

    def __str__(self):
        return self.school_name

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject: str, message: str, from_email: str = None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Teacher(models.Model):
    MR = 'MR'
    MS = 'MS'
    TITLE_CHOICES = [
        (None, gettext_lazy('None')),
        (MR, gettext_lazy('Mr.')),
        (MS, gettext_lazy('Ms.'))
    ]
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='teachers', related_query_name='teacher',
        verbose_name=gettext_lazy('school')
    )
    title = models.CharField(max_length=10, null=True, choices=TITLE_CHOICES, verbose_name=gettext_lazy('title'))
    first_name = models.CharField(max_length=50, verbose_name=gettext_lazy('first name'))
    last_name = models.CharField(max_length=50, verbose_name=gettext_lazy('last name'))

    class Meta:
        verbose_name = gettext_lazy('teacher')
        verbose_name_plural = gettext_lazy('teachers')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_name_with_title(self):
        return f'{self.get_title_display()} {self.first_name} {self.last_name}'


class Subject(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='subjects', related_query_name='subject',
        verbose_name=gettext_lazy('school')
    )
    # e.g. "Subject: _English_" or "Przedmiot: _angielski_"
    name = models.CharField(max_length=50, verbose_name=pgettext_lazy('inanimate name', 'name'))
    # e.g. "Who teaches you _English_?" or "Kto uczy cię _angielskiego_?"
    name_teacher_selection_case = models.CharField(
        max_length=50, null=True, default=None,
        verbose_name=gettext_lazy('name in "Who teaches you …?" case (e.g. "English")')
    )
    teachers = models.ManyToManyField(
        Teacher, related_name='subjects', related_query_name='subject', verbose_name=gettext_lazy('teachers')
    )

    class Meta:
        verbose_name = gettext_lazy('subject')
        verbose_name_plural = gettext_lazy('subjects')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['school', 'name'], name='unique_subject_name')
        ]

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='student_groups', related_query_name='student_group',
        verbose_name=gettext_lazy('school')
    )
    name = models.CharField(max_length=20, verbose_name=pgettext_lazy('inanimate name', 'name'))
    number_of_students = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name=gettext_lazy('number of students')
    )
    subjects = models.ManyToManyField(
        Subject, related_name='student_groups', related_query_name='student_group',
        verbose_name=gettext_lazy('subjects')
    )

    class Meta:
        verbose_name = gettext_lazy('group')
        verbose_name_plural = gettext_lazy('groups')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['school', 'name'], name='unique_student_group_name')
        ]

    def __str__(self):
        return self.name


class Assignment(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=gettext_lazy('school')
    )
    student_group = models.ForeignKey(
        StudentGroup, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=gettext_lazy('group')
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=gettext_lazy('subject')
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=gettext_lazy('teacher')
    )

    class Meta:
        verbose_name = gettext_lazy('assignment')
        verbose_name_plural = gettext_lazy('assignments')
        constraints = [
            models.UniqueConstraint(fields=['school', 'student_group', 'subject', 'teacher'], name='unique_assignment')
            # TODO: add teacher_belongs_to_subject and subject_belongs_to_group constraints
        ]

    def __str__(self):
        return f'{self.student_group} – {self.subject} – {self.teacher}'


class Question(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='questions', related_query_name='question',
        verbose_name=gettext_lazy('school')
    )
    position = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name=gettext_lazy('position')
    )
    text = models.CharField(max_length=100, verbose_name=gettext_lazy('text'))

    class Meta:
        verbose_name = gettext_lazy('question')
        verbose_name_plural = gettext_lazy('questions')
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(fields=['school', 'position'], name='unique_question_position'),
            models.UniqueConstraint(fields=['school', 'text'], name='unique_question_text'),
        ]

    def __str__(self):
        return self.text


class Completion(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='completions', related_query_name='completion',
        verbose_name=gettext_lazy('school')
    )
    student_group = models.ForeignKey(
        StudentGroup, on_delete=models.CASCADE, related_name='completions', related_query_name='completion',
        verbose_name=gettext_lazy('group')
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('added at'))

    class Meta:
        verbose_name = gettext_lazy('completion')
        verbose_name_plural = gettext_lazy('completions')

    def __str__(self):
        return gettext('completion') + ' ' + gettext('No.') + ' ' + str(self.id)


class Vote(models.Model):
    completion = models.ForeignKey(
        Completion, on_delete=models.CASCADE, related_name='votes', related_query_name='vote',
        verbose_name=gettext_lazy('completion')
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='votes', related_query_name='vote',
        verbose_name=gettext_lazy('question')
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='votes', related_query_name='vote',
        verbose_name=gettext_lazy('teacher')
    )
    mark = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)], verbose_name=pgettext_lazy('school mark', 'mark')
    )

    class Meta:
        verbose_name = gettext_lazy('vote')
        verbose_name_plural = gettext_lazy('votes')
        constraints = [
            models.UniqueConstraint(fields=['completion', 'question', 'teacher'], name='unique_vote')
            # TODO: add teacher_belongs_to_group constraint
        ]

    def __str__(self):
        return gettext('vote') + ' ' + gettext('No.') + ' ' + str(self.id)
