from datetime import datetime

from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from hashid_field import HashidAutoField

# TODO rename all fk to be more usable


# TODO make db migration files
class Questions(models.Model):
    id = HashidAutoField(primary_key=True)
    question = models.CharField(max_length=250, unique=True, error_messages={"unique": "This question already exists."})

    def __str__(self) -> str:
        return self.question


class Choices(models.Model):
    id = HashidAutoField(primary_key=True)
    choice = models.CharField(max_length=250)
    fk_question = models.ManyToManyField("apps.Questions")
    # TODO constrain of max 3-4 choices for question

    def __str__(self) -> str:
        return self.choice


class Answers(models.Model):
    id = HashidAutoField(primary_key=True)
    fk_question = models.OneToOneField("apps.Questions", on_delete=models.CASCADE)
    fk_choice = models.ForeignKey("apps.Choices", on_delete=models.CASCADE)  # correct choice

    # TODO constrains question has 1 choice for answer
    def __str__(self) -> str:
        return f"{self.fk_question} + {self.fk_choice}"


class UserQuestions(models.Model):
    id = HashidAutoField(primary_key=True)
    fk_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    fk_question = models.ForeignKey("apps.Questions", on_delete=models.CASCADE)
    time = models.DateTimeField(editable=False, default=datetime.now)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["fk_user", "fk_question"],
                name="unique_user_question",
            )
        ]


class UserAnswers(models.Model):
    id = HashidAutoField(primary_key=True)
    fk_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    fk_question = models.ForeignKey("apps.Questions", on_delete=models.CASCADE)
    fk_choice = models.ForeignKey("apps.Choices", on_delete=models.CASCADE, null=True)
    correct = models.BooleanField(editable=False, default=False)
    time = models.DateTimeField(editable=False, default=datetime.now)
    timeout = models.BooleanField(editable=False, default=False)

    #  TODO transaction signal


# TODO use signals to preserve user data or remove delete account
