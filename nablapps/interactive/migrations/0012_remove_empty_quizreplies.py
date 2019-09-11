from django.db import migrations

def remove_empty_quizreplies(apps, schema_editor):
    # Getting the historical `QuizReply` and `QuestionReply` model
    QuizReply = apps.get_model('interactive', 'QuizReply')
    QuestionReply = apps.get_model('interactive', 'QuestionReply')

    # Set of all seen quiz_reply_ids
    seen_ids = set()

    for question_reply in QuestionReply.objects.all():
        # Add each quiz_reply_id to the set
        seen_ids.add(question_reply.quiz_reply_id)

    # Remove quizreplies that are never referenced by a questionreply
    for quiz_reply in QuizReply.objects.all():
        if quiz_reply.id not in seen_ids:
            # Recalculate the score (to be absolutely certain)
            score = len([q for q in quiz_reply.questions.all() if q.is_correct])

            # Score has to be 0 when answering no questions
            if not (quiz_reply.score == score == 0):
                print(f"Quizreply with id {quiz_reply.id} had non-zero score, but had no questionreplies!")
                print("Consider deleting the quizreply manually.")

                # Skip this quizreply for manual intervention later
                continue

            # Remove the quizreply
            quiz_reply.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0011_update_quizreply_scores'),
    ]

    operations = [
            migrations.RunPython(remove_empty_quizreplies),
    ]


