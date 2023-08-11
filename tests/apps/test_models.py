# from django.test import TestCase
# from apps.models import Questions, Choices, Answers, UserQuestions, UserAnswers
# from django.db.utils import IntegrityError
# from django.utils import timezone
# from accounts.models import User


# class ModelsTestCase(TestCase):
#     def setUp(self):
#         self.user_data = {
#             "email": "test@example.com",
#             "name": "Test User",
#             "phone": "01234567891",
#             "password": "testpassword",
#         }
#         self.user = User.objects.create(**self.user_data)

#     def test_question_creation(self):
#         question_text = "What is the meaning of life?"
#         question = Questions.objects.create(question=question_text)
#         self.assertEqual(str(question), question_text)
#         self.assertIsNotNone(question.id)

#     def test_choice_creation(self):
#         question = Questions.objects.create(question="Sample question")
#         choice_text = "42"
#         choice = Choices.objects.create(choice=choice_text)
#         choice.question.add(question)
#         self.assertEqual(str(choice), choice_text)
#         self.assertIsNotNone(choice.id)
#         self.assertIn(question, choice.question.all())

#     def test_answer_creation(self):
#         question = Questions.objects.create(question="Sample question")
#         choice = Choices.objects.create(choice="Sample choice")
#         answer = Answers.objects.create(question=question, choice=choice)
#         self.assertEqual(str(answer), f"{question} + {choice}")

#     def test_user_questions_unique_constraint(self):
#         question = Questions.objects.create(question="Sample question")
#         UserQuestions.objects.create(user=self.user, questions=question)
#         with self.assertRaises(IntegrityError):
#             UserQuestions.objects.create(user=self.user, questions=question)

#     def test_user_answers_creation(self):
#         question = Questions.objects.create(question="Sample question")
#         choice = Choices.objects.create(choice="Sample choice")
#         user_answer = UserAnswers.objects.create(
#             user=self.user,
#             question=question,
#             choice=choice,
#             correct=False,
#             timeout=False,
#         )
#         self.assertTrue(isinstance(user_answer.time, timezone.datetime))
#         self.assertEqual(user_answer.user, self.user)
#         self.assertEqual(user_answer.question, question)
#         self.assertEqual(user_answer.choice, choice)
#         self.assertFalse(user_answer.correct)
#         self.assertFalse(user_answer.timeout)

#     def test_choices_constraint(self):
#         question = Questions.objects.create(question="Sample question")
#         choice1 = Choices.objects.create(choice="Choice 1")
#         choice2 = Choices.objects.create(choice="Choice 2")
#         choice3 = Choices.objects.create(choice="Choice 3")
#         question.question_choices.add(choice1, choice2, choice3)

#         self.assertEqual(question.question_choices.count(), 3)

#     def test_answers_constraint(self):
#         question = Questions.objects.create(question="Sample question")
#         choice = Choices.objects.create(choice="Sample choice")
#         answer = Answers.objects.create(question=question, choice=choice)
#         self.assertEqual(question.answer_question.choice, choice)
