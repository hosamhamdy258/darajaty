from django.core.management.base import BaseCommand, CommandError

from apps.management.commands.colors import colors_json
from apps.models import Answers, Choices, Questions


class Command(BaseCommand):
    help = "Creating Questions,Choices for testing"

    def handle(self, *args, **kwargs):
        try:
            colors = [color for color in colors_json.keys()]
            if len(colors) < 2:
                raise CommandError("List must has at least 2 elements")
            for index, color in enumerate(colors):
                question, _ = Questions.objects.get_or_create(question=f"Pick {color} from Choices ?")
                choices = [color, colors[index - 1], colors[index - 2]]
                for choice in choices:
                    instance, _ = Choices.objects.get_or_create(choice=choice)
                    instance.question.add(question)
                answer, _ = Answers.objects.get_or_create(choice=Choices.objects.get(choice=color), question=question)
        except Exception as e:
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS("Successfully questions created"))
