from django.db import models
from django.db.models.constraints import UniqueConstraint
from hashid_field import HashidAutoField


# Create your models here.


class Questions(models.Model):
    id = HashidAutoField(primary_key=True)
    question = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.question

    class Meta:
        ordering = ["id"]


class Choices(models.Model):
    id = HashidAutoField(primary_key=True)
    choice = models.CharField(max_length=250)
    question = models.ManyToManyField("apps.Questions", related_name="question_choices")
    # constrain of max 3-4 choices for question

    def __str__(self) -> str:
        return self.choice

    class Meta:
        ordering = ["id"]


class Answers(models.Model):
    id = HashidAutoField(primary_key=True)
    question = models.OneToOneField(
        "apps.Questions", related_name="answer_question", on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        "apps.Choices", related_name="answer_choice", on_delete=models.CASCADE
    )

    # constrains question has 1 choice for answer
    def __str__(self) -> str:
        return f"{self.question} + {self.choice}"

    class Meta:
        ordering = ["id"]


class UserQuestions(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(
        "accounts.User", related_name="user_questions", on_delete=models.CASCADE
    )
    questions = models.ForeignKey(
        "apps.Questions", related_name="questions_list", on_delete=models.CASCADE
    )
    time = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "questions"],
                name="unique_user_question",
            )
        ]

        ordering = ["id"]


class UserAnswers(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(
        "accounts.User", related_name="user_answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        "apps.Questions", related_name="chosen_question", on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        "apps.Choices", related_name="chosen_answer", on_delete=models.CASCADE
    )
    correct = models.BooleanField(editable=False, default=False)
    time = models.DateTimeField(editable=False, auto_now_add=True)
    timeout = models.BooleanField(editable=False, default=False)

    #  transaction
    class Meta:
        ordering = ["id"]


# TODO use signals to preserve user data or remove delete account
