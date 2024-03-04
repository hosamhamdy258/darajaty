from django.contrib import admin

from .models import Answers, Choices, Questions, UserAnswers, UserQuestions


class ChoicesInline(admin.TabularInline):
    model = Choices.fk_question.through
    extra = 0


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "question")
    inlines = [
        ChoicesInline,
    ]


@admin.register(Choices)
class ChoicesAdmin(admin.ModelAdmin):
    list_display = ("id", "choice")
    list_filter = ("fk_question",)


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "fk_question", "fk_choice")
    list_filter = ("fk_question", "fk_choice")


@admin.register(UserQuestions)
class UserQuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "fk_user", "fk_question", "time")
    list_filter = ("fk_user", "fk_question", "time")
    readonly_fields = ("time",)


@admin.register(UserAnswers)
class UserAnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "fk_user", "fk_question", "fk_choice", "time", "correct", "timeout")
    list_filter = ("fk_user", "fk_question", "fk_choice", "time")
    readonly_fields = ("correct", "time", "timeout")
