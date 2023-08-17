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
        self.questions_list = Questions.objects.exclude(
            questions_list__user=self.request.user
        )[:1]
        if len(self.questions_list) == 0:
            raise ParseError(detail="No Available Questions Try Again Later")
        return self.questions_list

    def list(self, request, *args, **kwargs):
        self.question_counter(request)
        response = super().list(request, *args, **kwargs)
        UserQuestions.objects.create(
            questions=self.questions_list[0], user=self.request.user
        )
        response.data = response.data[0] if len(response.data) == 1 else response.data

        return response

    def question_counter(self, request):
        questionsToday = UserQuestions.objects.filter(
            user=request.user, time__gte=datetime.now().date()
        ).count()
        # TODO add dynamic field with for changing max allowed questions per day
        if questionsToday >= 2:
            raise ParseError(detail="Reached Max Allowed Questions Per Day")


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
