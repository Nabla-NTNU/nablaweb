from django.db import models
from .base import InteractiveElement


class Test(InteractiveElement):
    
    questions = models.ManyToManyField(
        "interactive.TestQuestion"
    )

    results = models.ManyToManyField(
        "interactive.TestResult"
    )

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

    alternatives = models.ManyToManyField(
        "interactive.TestQuestionAlternative"
    )

    def to_map(self):
        alternatives = []
        for a in self.alternatives.all():
            alternatives.append(a.text)
        return alternatives


class TestQuestionAlternative(models.Model):

    text = models.TextField()


class TestResult(models.Model):
    
    title = models.CharField(
        max_length=100
    )

    content = models.TextField()

    def to_map():
        map = {}
        map.put("name", title)
        map.put("text", content)
        return map

