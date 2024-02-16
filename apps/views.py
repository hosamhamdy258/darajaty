import random
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from apps.models import Questions, UserAnswers, UserQuestions
from apps.serializers.questions_answers import (
    Questions_serializers,
    User_Answers_serializers,
)
from apps.serializers.questions_create import Questions_create_serializers

# Create your views here.

timeout = settings.ANSWER_TIMEOUT


class Questions_view(CreateAPIView):
    serializer_class = Questions_create_serializers
    queryset = Questions.objects.all()


class Today_Question_view(ListAPIView):
    serializer_class = Questions_serializers
    pagination_class = None

    def get_queryset(self):
        # * question choice logic
        self.questions_list = Questions.objects.exclude(
            questions_list__user=self.request.user
        )[:1]
        if len(self.questions_list) == 0:
            raise ParseError(detail="No Available Questions Try Again Later")

        # TODO check for last question is answered if not return it again to continue timer on frontend

        return self.questions_list

    def list(self, request, *args, **kwargs):
        user = request.user
        object_counter(
            user=user,
            model=UserQuestions,
            times=100,
            msg="Reached Max Allowed Questions Per Day",
        )

        last_question = self.verify_last_question(user)
        if last_question:
            serializer = self.get_serializer(last_question.questions)
            response = Response(serializer.data)
            random.shuffle(response.data["choices_set"])
            time = last_question.time + timedelta(seconds=timeout) - timezone.now()
            response.data["time"] = time.total_seconds().__ceil__()
            return response

        response = super().list(request, *args, **kwargs)

        response.data = response.data[0] if len(response.data) == 1 else response.data
        random.shuffle(response.data["choices_set"])

        UserQuestions.objects.create(questions=self.questions_list[0], user=user)
        response.data["time"] = timeout

        return response

    def verify_last_question(self, user):
        last_question = UserQuestions.objects.filter(user=user).last()
        if last_question:
            try:
                UserAnswers.objects.get(question=last_question.questions, user=user)
            except ObjectDoesNotExist:
                if timezone.now() - last_question.time > timedelta(seconds=timeout):
                    # TODO Equalize UserAnswers with UserQuestions to ensure consistency data on transactions table
                    UserAnswers.objects.create(
                        question=last_question.questions, user=user
                    )

                else:
                    return last_question


class Today_Answer_view(CreateAPIView):
    serializer_class = User_Answers_serializers
    pagination_class = None

    # TODO check requested Question is submitted answer
    def post(self, request, *args, **kwargs):
        user = request.user
        object_counter(
            user=user,
            model=UserAnswers,
            times=100,
            msg="Reached Max Allowed Answers Per Day",
        )

        return super().post(request, *args, **kwargs)


# class Choices_view(models.Model):

# class Answers_view(models.Model):


def object_counter(user, model, times, msg):
    counted_objects = model.objects.filter(
        user=user, time__gte=datetime.now().date()
    ).count()
    # TODO add dynamic field with for changing max allowed times per day
    if counted_objects >= times:
        raise ParseError(detail=msg)
