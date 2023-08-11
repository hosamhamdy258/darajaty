from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.models import Answers, Choices, Questions, UserAnswers, UserQuestions


class User_Answers_serializers(FlexFieldsModelSerializer):
    # id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     pk_field=HashidSerializerCharField(source_field=HashidField()),
    #     required=False,
    #     write_only=True,
    # )
    choice = serializers.PrimaryKeyRelatedField(
        queryset=Choices.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        write_only=True,
    )
    question = serializers.PrimaryKeyRelatedField(
        queryset=Questions.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        write_only=True,
    )

    class Meta:
        model = UserAnswers
        fields = ("choice", "question", "correct", "timeout")
        read_only_fields = ("correct", "timeout")

    def create(self, validated_data):
        user = self.context["request"].user
        question = self.check_question_answer_flow(validated_data, user)

        try:
            obj = UserAnswers.objects.get(
                question=validated_data["question"], user=user
            )
            print(obj)
        except ObjectDoesNotExist:
            ParseError(detail="Already Answered this question")

        if datetime.now() - question.time > timedelta(seconds=40):
            validated_data.update(timeout=True)

        # * check answer is correct
        try:
            Answers.objects.get(
                question=validated_data["question"], choice=validated_data["choice"]
            )
            validated_data.update(correct=True)
        except ObjectDoesNotExist:
            pass

        validated_data.update(user=user)
        instance = super().create(validated_data)
        if instance.timeout:
            raise ParseError(detail="Time Ran out to answer")

        if instance.correct:
            user.wallet.deposit(5)

        return instance

    def check_question_answer_flow(self, validated_data, user):
        try:
            return UserQuestions.objects.get(
                user=user, questions=validated_data["question"]
            )
        except ObjectDoesNotExist:
            raise ParseError(detail="Must Request Question before attempting to answer")


class Answers_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = Answers
        fields = ("id", "answer", "question")


class Choices_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = Choices
        fields = ("id", "choice")


class Questions_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    question_choices = Choices_serializers(many=True)

    class Meta:
        model = Questions
        fields = ("id", "question", "question_choices")
        # expandable_fields = {"choices": ("Choices_serializers", {"many": True})}

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     print(rep)
    #     return rep
