from django.db import models
from .base import InteractiveElement


class Test(InteractiveElement):

    def to_map(self):
        map = {}
        questions = []
        for q in self.questions.all():
            questions.append(q.to_map())
        map.put("questions", questions)

        results = []
        for r in self.results.all():
            results.append(r.to_map())
        map.put("results", results)
        return map


class TestQuestion(models.Model):

    text = models.TextField()

    test = models.ForeignKey(
        "Test",
        related_name="questions"
    )

    def to_map(self):
        alternatives = []
        for a in self.alternatives.all():
            alternatives.append(a.text)
        return alternatives


class TestQuestionAlternative(models.Model):

    text = models.TextField()

    question = models.ForeignKey(
        'TestQuestion',
        related_name="alternatives")


class TestResult(models.Model):
    
    title = models.CharField(
        max_length=100
    )

    content = models.TextField()

    test = models.ForeignKey(
        "Test",
        related_name="results"
    )

    def to_map():
        map = {}
        map.put("name", title)
        map.put("text", content)
        return map

