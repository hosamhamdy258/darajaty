from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.models import Answers, Questions, UserAnswers, UserQuestions, Choices
from core.settings.base import REST_FRAMEWORK

User = get_user_model()


# # class QuestionsViewTest(APITestCase):
# # def test_create_question(self):
# #     url = reverse("questions-list")
# #     data = {"question": "What is your favorite color?"}
# #     response = self.client.post(url, data, format="json")
# #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #     self.assertEqual(Questions.objects.count(), 1)
# #     self.assertEqual(
# #         Questions.objects.get().question, "What is your favorite color?"
# #     )

# # def test_list_questions(self):
# #     url = reverse("questions-list")
# #     response = self.client.get(url)
# #     self.assertEqual(response.status_code, status.HTTP_200_OK)


# class TodayQuestionViewTest(APITestCase):
#     def setUp(self):
#         self.valid_data = {
#             "name": "Test User",
#             "password": "StrongPassword123",
#             "email": "test@example.com",
#             "phone": "01234567890",
#         }
#         self.user = User.objects.create_user(**self.valid_data)

#     def test_get_today_question_no_available(self):
#         # self.client.force_login(self.user)
#         self.client.force_authenticate(user=self.user)
#         url = "/api/today_question/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data["detail"], "No Available Questions Today Try Again Tomorrow"
#         )

#     def test_get_today_question_max_allowed_questions(self):
#         self.client.force_login(self.user)
#         self.client.force_authenticate(user=self.user)
#         Questions.objects.create(question="What is your favorite color?")
#         UserQuestions.objects.create(
#             user=self.user, questions=Questions.objects.first()
#         )
#         url = "/api/today_question/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data["detail"], "Reached Max Allowed Questions Per Day"
#         )

#     def test_get_today_question_success(self):
#         self.client.force_login(self.user)
#         self.client.force_authenticate(user=self.user)

#         Questions.objects.create(question="What is your favorite color?")
#         url = "/api/today_question/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodayAnswerViewTest(APITestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test User",
            "password": "StrongPassword123",
            "email": "test@example.com",
            "phone": "01234567890",
        }
        self.user = User.objects.create_user(**self.valid_data)
        self.choice = Choices.objects.create(choice="Blue")
        self.question = Questions.objects.create(
            question="What is your favorite color?"
        )
        self.choice.question.add(self.question)
        Answers.objects.create(question=self.question, choice=self.choice)
        self.url = "/api/today_answer/"
        self.client.force_login(self.user)
        self.client.force_authenticate(user=self.user)
        self.get_url = "/api/today_question/"
        self.get_response = self.client.get(self.get_url)

    def test_post_today_answer_max_allowed_answers(self):
        UserAnswers.objects.create(
            user=self.user, question=self.question, choice=self.choice
        )
        data = {"question": self.question.id, "choice": "Red"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Reached Max Allowed Answers Per Day")

    # def test_post_today_answer_success(self):
    #     data = {"question": self.question.id, "choice": self.choice.id}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_post_today_answer_with_attempts(self):
    #     self.client.force_login(self.user)
    #     UserAnswers.objects.create(
    #         user=self.user, question=self.question, choice=self.choice
    #     )
    #     data = {"question": self.question.id, "choice": "Red"}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data["detail"], "Reached Max Allowed Answers Per Day")
