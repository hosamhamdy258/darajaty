from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.models import Questions, UserAnswers, UserQuestions
from apps.serializers.questions_create import Questions_create_serializers
from apps.serializers.questions_answers import (
    Questions_serializers,
    User_Answers_serializers,
)

# Create your views here.


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
        return self.questions_list

    def list(self, request, *args, **kwargs):
        user = request.user
        object_counter(
            user=user,
            model=UserQuestions,
            times=22,
            msg="Reached Max Allowed Questions Per Day",
        )

        self.verify_last_question(user)

        response = super().list(request, *args, **kwargs)

        response.data = response.data[0] if len(response.data) == 1 else response.data
        UserQuestions.objects.create(questions=self.questions_list[0], user=user)
        # TODO check randomness of order of choices list
        return response

    def verify_last_question(self, user):
        last_question = UserQuestions.objects.filter(user=user).last()
        if last_question:
            try:
                UserAnswers.objects.get(question=last_question.questions, user=user)
            except ObjectDoesNotExist:
                if datetime.now() - last_question.time > timedelta(seconds=30):
                    UserAnswers.objects.create(
                        question=last_question.questions, user=user
                    )
                else:
                    raise ParseError(
                        detail="Answer last Question before request new question"
                    )


class Today_Answer_view(CreateAPIView):
    serializer_class = User_Answers_serializers
    pagination_class = None

    # TODO check requested Question is submitted answer
    def post(self, request, *args, **kwargs):
        user = request.user
        object_counter(
            user=user,
            model=UserAnswers,
            times=22,
            msg="Reached Max Allowed Answers Per Day",
        )

        response = super().post(request, *args, **kwargs)

        return response


# class Choices_view(models.Model):

# class Answers_view(models.Model):


def object_counter(user, model, times, msg):
    counted_objects = model.objects.filter(
        user=user, time__gte=datetime.now().date()
    ).count()
    # TODO add dynamic field with for changing max allowed times per day
    if counted_objects >= times:
        raise ParseError(detail=msg)
