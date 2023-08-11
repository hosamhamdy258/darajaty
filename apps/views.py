from datetime import datetime

from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView

from apps.models import Questions, UserAnswers, UserQuestions
from apps.serializers import Questions_serializers, User_Answers_serializers

# Create your views here.


class Questions_view(ListCreateAPIView):
    serializer_class = Questions_serializers
    queryset = Questions.objects.all()


class Today_Question_view(ListAPIView):
    serializer_class = Questions_serializers
    pagination_class = None

    def get_queryset(self):
        # * question choice logic
        questions_list = Questions.objects.exclude(
            questions_list__user=self.request.user
        )[:1]
        if questions_list.count() == 0:
            raise ParseError(detail="No Available Questions Today Try Again Tomorrow")
        return questions_list

    def list(self, request, *args, **kwargs):
        questionsToday = UserQuestions.objects.filter(
            user=request.user, time__gte=datetime.now().date()
        )
        # TODO add parameter for changing max allowed questions per day

        if questionsToday.exists():
            raise ParseError(detail="Reached Max Allowed Questions Per Day")

        response = super().list(request, *args, **kwargs)
        UserQuestions.objects.create(
            questions=self.get_queryset().first(), user=self.request.user
        )
        response.data = response.data[0] if len(response.data) == 1 else response.data

        return response


class Today_Answer_view(CreateAPIView):
    serializer_class = User_Answers_serializers
    pagination_class = None

    # TODO check requested Question is submitted answer
    def post(self, request, *args, **kwargs):
        user = request.user
        self.check_attempts(user)

        response = super().post(request, *args, **kwargs)

        return response

    def check_attempts(self, user):
        attemptsToday = UserAnswers.objects.filter(
            user=user, time__gte=datetime.now().date()
        )
        # TODO add parameter for changing max allowed answers per day

        if attemptsToday.exists():
            raise ParseError(detail="Reached Max Allowed Answers Per Day")


# class Choices_view(models.Model):

# class Answers_view(models.Model):
