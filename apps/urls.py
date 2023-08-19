from django.urls import path

from apps.views import Questions_view, Today_Answer_view, Today_Question_view

app_name = "apps"
urlpatterns = [
    path("questions/", Questions_view.as_view()),
    path("today_question/", Today_Question_view.as_view()),
    path("today_answer/", Today_Answer_view.as_view()),
]
