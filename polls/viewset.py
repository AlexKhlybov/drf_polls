import django_filters
from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import AnswerTracker, Question, Quiz
from .serializers import (
    AnswerSerializer,
    AnswerTrackerListSerializer,
    AnswerTrackerSerializer,
    QuestionSerializer,
    QuizSerializer,
)


class AnswerFilterSet(django_filters.FilterSet):
    customer = django_filters.Filter(field_name="customer")

    class Meta:
        model = AnswerTracker
        fields = [
            "customer",
        ]


class QuizzesViewSet(ModelViewSet):
    """Опросы"""

    queryset = Quiz.get_active()
    serializer_class = QuizSerializer
    permission_classes_by_action = {
        "list": [permissions.AllowAny],
        "retrieve": [permissions.AllowAny],
        "create": [permissions.IsAdminUser],
        "update": [permissions.IsAdminUser],
        "destroy": [permissions.IsAdminUser],
        "partial_update": [permissions.IsAdminUser],
        "partial_destroy": [permissions.IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class QuestionViesSet(ModelViewSet):
    """Вопросы"""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes_by_action = {
        "list": [permissions.AllowAny],
        "retrieve": [permissions.AllowAny],
        "create": [permissions.IsAdminUser],
        "update": [permissions.IsAdminUser],
        "destroy": [permissions.IsAdminUser],
        "partial_update": [permissions.IsAdminUser],
        "partial_destroy": [permissions.IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class AnswerTrakerViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """Ответы пользователей"""

    queryset = AnswerTracker.objects.all()
    serializer_class = AnswerTrackerSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = AnswerFilterSet
    permission_classes_by_action = {
        "list": [permissions.AllowAny],
        "retrieve": [permissions.AllowAny],
        "create": [permissions.AllowAny],
        "update": [permissions.IsAdminUser],
        "destroy": [permissions.IsAdminUser],
        "partial_update": [permissions.IsAdminUser],
        "partial_destroy": [permissions.IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return AnswerTrackerSerializer
        if self.action == "list":
            return AnswerTrackerListSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        parsed_answers = self.parse_request(request)
        serialized_answers = AnswerTrackerSerializer(data=parsed_answers, many=True)
        if serialized_answers.is_valid(raise_exception=True):
            serialized_answers.save()
            return Response(serialized_answers.data, status=status.HTTP_201_CREATED)
        return Response(serialized_answers.errors, status=status.HTTP_400_BAD_REQUEST)

    def parse_request(self, request):
        parsed_answers = []
        if request:
            answer = dict()
            answer["quiz_id"] = request.data["quiz_id"]
            answer["customer"] = request.data["customer"]
            answer["question_id"] = request.data["question_id"]
            answer["answer_text"] = request.data.get("answer_text", "")
            if request.data.get("choice_id"):
                for choice in request.data["choice_id"]:
                    answer["choice_id"] = choice
                    parsed_answers.append(answer.copy())
            else:
                parsed_answers.append(answer.copy())
        return parsed_answers

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        customer = request.query_params.get("customer")
        report = get_list_or_404(AnswerTracker, customer=customer)
        serialized_report = AnswerSerializer(report, many=True)
        parsed_report = self.parse_report(serialized_report.data)
        return Response(parsed_report)

    def parse_report(self, serialized_report):
        quizzes = set(answer["quiz_id"] for answer in serialized_report)
        parsed_report: dict = {quiz: [] for quiz in quizzes}
        for answer in serialized_report:
            parsed_report[answer.pop("quiz_id")] = answer
        return parsed_report
