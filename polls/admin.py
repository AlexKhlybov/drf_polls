import nested_admin
from django.contrib import admin

from .models import AnswerTracker, Choice, Question, Quiz


class ChoiceInLine(nested_admin.NestedStackedInline):
    model = Choice
    extra = 0


class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInLine]


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ["title", "start_date", "end_date"]
    save_on_top = True
    fieldsets = [
        (None, {"fields": ["title", "description"]}),
        (
            "Dates",
            {
                "fields": [
                    ("start_date", "end_date"),
                ]
            },
        ),
    ]
    inlines = [QuestionInLine]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("start_date",)
        return self.readonly_fields


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    pass


@admin.register(AnswerTracker)
class AnswerTrackerAdmin(nested_admin.NestedModelAdmin):
    pass
