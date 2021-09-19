from rest_framework.routers import DefaultRouter

from . import viewset

router = DefaultRouter()

router.register("polls", viewset.QuizzesViewSet)
router.register("questions", viewset.QuestionViesSet)
router.register("answer", viewset.AnswerTrakerViewSet)


urlpatterns = router.urls
