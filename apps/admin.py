from django.contrib import admin

from .models import Answers, Choices, Questions, UserAnswers, UserQuestions


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "question")


@admin.register(Choices)
class ChoicesAdmin(admin.ModelAdmin):
    list_display = ("id", "choice")
    list_filter = ("question",)


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "choice")
    list_filter = ("question", "choice")


@admin.register(UserQuestions)
class UserQuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "questions", "time")
    list_filter = ("user", "questions", "time")
    readonly_fields = ("time",)


@admin.register(UserAnswers)
class UserAnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "choice", "time", "correct", "timeout")
    list_filter = ("user", "question", "choice", "time")
    readonly_fields = ("correct", "time", "timeout")
