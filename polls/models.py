from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", blank=True)
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title

    def clean(self):
        """Проверка даты"""
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("Закончиться не может раньше чем начаться")

    @staticmethod
    def get_active():
        today = timezone.now().date()
        active_quizzes = Quiz.objects.filter(start_date__gte=today)
        return active_quizzes


class Question(models.Model):
    class QUESTIONSTYPE:
        TEXT = "Текст"
        ONE = "Одиночный выбор"
        MULTI = "Множественный выбор"
        TYPES = ((TEXT, "Текст"), (ONE, "Одиночный выбор"), (MULTI, "Множественный выбор"))

    quiz_id = models.ForeignKey(Quiz, verbose_name="Опрос", on_delete=models.CASCADE)
    question_text = models.CharField(verbose_name="Вопрос", max_length=1000)
    question_type = models.CharField(
        verbose_name="Тип вопроса", max_length=128, choices=QUESTIONSTYPE.TYPES, default=QUESTIONSTYPE.ONE
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question_id = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name="Ответ", max_length=1000)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.choice_text


class AnswerTracker(models.Model):
    customer = models.ForeignKey(get_user_model(), verbose_name="Пользователь", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, verbose_name="Опрос", on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choice, verbose_name="Ответ", on_delete=models.CASCADE, blank=True, null=True)
    answer_text = models.TextField(verbose_name="Текст ответа", blank=True)

    class Meta:
        verbose_name = "История ответов"
        verbose_name_plural = "История ответов"

    def clean(self):
        super().clean()
        if not any([self.choice_id, self.answer_text]):
            raise ValidationError("Поля для выбора ответов или текстовые поля должны быть заполнены")

    def __str__(self):
        return f"{self.customer} - {self.question_id} - {self.choice_id or self.answer_text}"
