from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AnswerTracker, Choice, Question, Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text"]


class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Question
        fields = ["id", "question_text", "question_type", "choice_set"]


class AnswerTrackerSerializer(serializers.ModelSerializer):
    choice_id = ChoiceSerializer(read_only=True)

    class Meta:
        model = AnswerTracker
        fields = ["id", "customer", "quiz_id", "question_id", "choice_id", "answer_text"]


class AnswerTrackerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    quiz_id = serializers.SerializerMethodField("get_quiz_title")
    question_id = serializers.SerializerMethodField("get_question_text")
    answer_text = serializers.CharField()
    choice_id = serializers.SerializerMethodField("get_choice_text")

    def get_quiz_title(self, obj):
        return obj.quiz_id.title

    def get_question_text(self, obj):
        return obj.question_id.question_text

    def get_choice_text(self, obj):
        return obj.choice_id.choice_text if obj.choice_id else None

    class Meta:
        model = AnswerTracker
        fields = [
            "quiz_id",
            "question_id",
            "choice_id",
            "answer_text",
        ]


class AnsweredQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTracker
        fields = ["question_id", "choice_id", "answer_text"]
