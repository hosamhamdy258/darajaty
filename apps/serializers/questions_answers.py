from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.models import Answers, Choices, Questions, UserAnswers, UserQuestions

answer_tolerance = settings.TOLERANCE_TIME


class User_Answers_serializers(FlexFieldsModelSerializer):
    # id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     pk_field=HashidSerializerCharField(source_field=HashidField()),
    #     required=False,
    #     write_only=True,
    # )
    fk_choice = serializers.PrimaryKeyRelatedField(
        queryset=Choices.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        write_only=True,
    )
    fk_question = serializers.PrimaryKeyRelatedField(
        queryset=Questions.objects.all(),
        pk_field=HashidSerializerCharField(source_field=HashidField()),
        write_only=True,
    )
    wallet = serializers.IntegerField(source="fk_user.wallet.current_balance", required=False, read_only=True)

    class Meta:
        model = UserAnswers
        fields = ("fk_choice", "fk_question", "correct", "timeout", "wallet")
        read_only_fields = ("correct", "timeout")

    def create(self, validated_data):
        user = self.context["request"].user
        question = self.check_question_answer_flow(validated_data, user)

        self.is_answered_before(validated_data, user)

        if datetime.now() - question.time > timedelta(seconds=answer_tolerance):
            validated_data.update(timeout=True)

        # * check answer is correct
        try:
            Answers.objects.get(fk_question=validated_data["fk_question"], fk_choice=validated_data["fk_choice"])
            validated_data.update(correct=True)
        except ObjectDoesNotExist:
            pass

        validated_data.update(fk_user=user)
        instance = super().create(validated_data)
        if instance.timeout:
            raise ParseError(detail="Time Ran out to answer")

        if instance.correct:
            user.wallet.deposit(5)

        return instance

    def is_answered_before(self, validated_data, user):
        query = UserAnswers.objects.filter(fk_question=validated_data["fk_question"], fk_user=user).exists()
        if query:
            raise ParseError(detail="Already Answered this question")

    def check_question_answer_flow(self, validated_data, user):
        try:
            return UserQuestions.objects.get(fk_user=user, fk_question=validated_data["fk_question"])
        except ObjectDoesNotExist:
            raise ParseError(detail="Must Request Question before attempting to answer")


class Answers_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = Answers
        fields = ("id", "fk_answer", "fk_question")


class Choices_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = Choices
        fields = ("id", "choice")


class Questions_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    choices_set = Choices_serializers(many=True)

    class Meta:
        model = Questions
        fields = ("id", "question", "choices_set")
        # expandable_fields = {"choices": ("Choices_serializers", {"many": True})}
