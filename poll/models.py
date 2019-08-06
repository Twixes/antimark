from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext, gettext_lazy, pgettext_lazy


class Teacher(models.Model):
    MR = 'MR'
    MS = 'MS'
    TITLE_CHOICES = [
        (MR, gettext_lazy('Mr.')),
        (MS, gettext_lazy('Ms.'))
    ]
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, verbose_name=gettext_lazy('title'))
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
    # e.g. "Subject: _English_" or "Przedmiot: _angielski_"
    name = models.CharField(max_length=50, unique=True, verbose_name=pgettext_lazy('subject name', 'name'))
    # e.g. "Who teaches you _English_?" or "Kto uczy cię _angielskiego_?"
    name_teacher_selection_case = models.CharField(
        max_length=50, null=True, verbose_name=gettext_lazy('name in "Who teaches you …?" case (e.g. "English")')
    )
    teachers = models.ManyToManyField(
        Teacher, related_name='subjects', related_query_name='subject', verbose_name=gettext_lazy('teachers')
    )

    class Meta:
        verbose_name = gettext_lazy('subject')
        verbose_name_plural = gettext_lazy('subjects')
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    identifier = models.CharField(unique=True, max_length=10, verbose_name=gettext_lazy('identifier'))
    number_of_students = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name=gettext_lazy('number of students')
    )
    subjects = models.ManyToManyField(
        Subject, related_name='groups', related_query_name='group', verbose_name=gettext_lazy('subjects')
    )

    class Meta:
        verbose_name = gettext_lazy('group')
        verbose_name_plural = gettext_lazy('groups')
        ordering = ['identifier']

    def __str__(self):
        return self.identifier


class Assignment(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='assignments', related_query_name='assignment',
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
            models.UniqueConstraint(fields=['group', 'subject', 'teacher'], name='unique_assignment')
            # TODO: add teacher_belongs_to_subject and subject_belongs_to_group constraints
        ]

    def __str__(self):
        return f'{self.group} – {self.subject} – {self.teacher}'


class Question(models.Model):
    text = models.CharField(max_length=100, unique=True, verbose_name=gettext_lazy('text'))
    position = models.PositiveSmallIntegerField(
        unique=True, default=1, validators=[MinValueValidator(1)], verbose_name=gettext_lazy('position')
    )

    class Meta:
        verbose_name = gettext_lazy('question')
        verbose_name_plural = gettext_lazy('questions')
        ordering = ['position']

    def __str__(self):
        return self.text


class Completion(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=gettext_lazy('group')
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('added at'))

    class Meta:
        verbose_name = gettext_lazy('completion')
        verbose_name_plural = gettext_lazy('completions')

    def __str__(self):
        return gettext('completion') + ' ' + gettext('No.') + ' ' + str(self.id)


class Vote(models.Model):
    completion = models.ForeignKey(
        Completion, on_delete=models.CASCADE,
        related_name='votes', related_query_name='vote', verbose_name=gettext_lazy('question')
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=gettext_lazy('question')
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='votes', related_query_name='vote', verbose_name=gettext_lazy('teacher')
    )
    mark = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name=pgettext_lazy('school mark', 'mark')
    )

    class Meta:
        verbose_name = gettext_lazy('vote')
        verbose_name_plural = gettext_lazy('votes')
        constraints = [
            models.UniqueConstraint(fields=['completion', 'question', 'teacher'], name='unique_assignment')
            # TODO: add teacher_belongs_to_group constraint
        ]

    def __str__(self):
        return gettext('vote') + ' ' + gettext('No.') + ' ' + str(self.id)
