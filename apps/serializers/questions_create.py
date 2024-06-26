from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from apps.models import Answers, Choices, Questions
from core.extensions.utils import check_value_exists, duplicated_value_checker


class Choices_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    correct = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Choices
        fields = ("id", "choice", "correct")


class Answer_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    fk_choice = Choices_create_serializers()

    class Meta:
        model = Answers
        fields = ["id", "fk_choice"]


class Questions_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    choices_set = Choices_create_serializers(many=True)
    answer_question = Answer_create_serializers(read_only=True)

    class Meta:
        model = Questions
        fields = ("id", "question", "choices_set", "answer_question")

    def create(self, validated_data):
        choices = validated_data.pop("choices_set")
        duplicated_value_checker(iterable=choices, keys={"correct": True, "choice": None})
        check_value_exists(
            iterable=choices,
            key="correct",
            error_msg="one of choices must has correct:true",
        )
        # TODO question must has 2 choices at least
        question_instance = super().create(validated_data)
        for choice in choices:
            correct = choice.pop("correct")
            choice_instance, _ = Choices.objects.get_or_create(**choice)
            choice_instance.fk_question.add(question_instance)
            if correct:
                Answers.objects.create(fk_question=question_instance, fk_choice=choice_instance)

        return question_instance
