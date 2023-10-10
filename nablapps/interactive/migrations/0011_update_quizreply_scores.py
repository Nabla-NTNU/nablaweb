from django.db import migrations


def is_correct(question_reply):
    # `is_correct` method from `Question_Reply`
    return question_reply.question.correct_alternative == question_reply.alternative


def get_correct_count(quiz_reply):
    # `get_correct_count` method from `Quiz_Reply`
    return len([q for q in quiz_reply.questions.all() if is_correct(q)])


def update_scores(apps, schema_editor):
    # Getting the historical `QuizReply` model
    QuizReply = apps.get_model("interactive", "QuizReply")

    for reply in QuizReply.objects.all():
        reply.score = get_correct_count(reply)
        reply.save()


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0010_auto_20190205_1436"),
    ]

    operations = [
        migrations.RunPython(update_scores),
    ]
