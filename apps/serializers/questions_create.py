from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers


from apps.models import Answers, Choices, Questions
from core.extensions.utils import duplicated_value_checker


class Choices_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    correct = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Choices
        fields = ("id", "choice", "correct")


class Answer_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    choice = Choices_create_serializers()

    class Meta:
        model = Answers
        fields = ["id", "choice"]


class Questions_create_serializers(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    question_choices = Choices_create_serializers(many=True)
    answer_question = Answer_create_serializers(read_only=True)

    class Meta:
        model = Questions
        fields = ("id", "question", "question_choices", "answer_question")

    def create(self, validated_data):
        choices = validated_data.pop("question_choices")
        duplicated_value_checker(iterable=choices, key="correct", value=True)
        question_instance = super().create(validated_data)
        for choice in choices:
            correct = choice.pop("correct")
            choice_instance = Choices.objects.create(**choice)
            choice_instance.question.add(question_instance)
            if correct:
                Answers.objects.create(
                    question=question_instance, choice=choice_instance
                )

        return question_instance
