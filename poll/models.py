from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _, pgettext_lazy as p_


class Teacher(models.Model):
    MR = 'MR'
    MS = 'MS'
    TITLE_CHOICES = [
        (MR, _('Mr.')),
        (MS, _('Ms.'))
    ]
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, verbose_name=_('title'))
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.get_title_display()} {self.first_name} {self.last_name}'


class Subject(models.Model):
    # e.g. "Subject: _English_" or "Przedmiot: _angielski_"
    name = models.CharField(max_length=50, unique=True, verbose_name=p_('subject name', 'name'))
    # e.g. "Who teaches you _English_?" or "Kto uczy cię _angielskiego_?"
    name_teacher_selection_case = models.CharField(
        max_length=50, null=True, verbose_name=_('name in "Who teaches you …?" case (e.g. "English")')
    )
    teachers = models.ManyToManyField(
        Teacher, related_name='subjects', related_query_name='subject', verbose_name=_('teachers')
    )

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    identifier = models.CharField(max_length=10, verbose_name=_('identifier'))
    number_of_students = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_('number of students')
    )
    subjects = models.ManyToManyField(
        Subject, related_name='groups', related_query_name='group', verbose_name=_('subjects')
    )

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ['identifier']

    def __str__(self):
        return self.identifier


class Assignment(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=_('teacher')
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=_('group')
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
        verbose_name=_('subject')
    )

    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'group', 'subject'], name='unique_assignment')
        ]

    def __str__(self):
        return f'{self.teacher} – {self.group} – {self.subject}'


class Question(models.Model):
    text = models.CharField(max_length=100, unique=True, verbose_name=_('text'))
    position = models.PositiveSmallIntegerField(
        unique=True, validators=[MinValueValidator(1)], verbose_name=_('position')
    )

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ['position']

    def __str__(self):
        return self.text


class Vote(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=_('question')
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=_('teacher')
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=_('group')
    )
    mark = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name=p_('school mark', 'mark')
    )
    cast_at = models.DateTimeField(auto_now_add=True, verbose_name=_('cast at'))

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')

    def __str__(self):
        return f'{self.question.position}. – {self.teacher} – {self.group} – {self.mark}'
