from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from .base import InteractiveElement


class Test(InteractiveElement):
    """
    Represents a user-made test
    """

    title = models.TextField(
        blank=False,
        default="",
        verbose_name="tittel",
        help_text="Tittel på brukertesten",
    )

    published = models.NullBooleanField(
        default=True,
        verbose_name="Publisert",
    )

    class Meta:
        verbose_name = "brukertest"
        verbose_name_plural = "brukertester"

    def get_absolute_url(self):
        return reverse("user_test", kwargs={"pk": self.id})

    def __str__(self):
        return str(self.title)


class TestQuestion(models.Model):

    text = models.TextField(blank=False, default="", verbose_name="spørsmål")

    test = models.ForeignKey(
        "Test", null=True, on_delete=models.CASCADE, related_name="questions"
    )

    def changeform_link(self):
        if self.id:
            changeform_url = reverse(
                "admin:interactive_testquestion_change", args=(self.id,)
            )
            liste = "<ul>"
            for alt in self.alternatives.all():
                liste += "<li>" + str(alt.text) + " - "
                for result in alt.get_target_with_weights():
                    liste += str(result[0]) + "[" + str(result[1]) + "], "
                liste = liste[:-2]
            liste += "</ul>"
            return mark_safe(
                '<a href="%s" target="_blank">Endre alternativer</a>' % changeform_url
                + liste
            )
        return (
            "Du må lagre (og fortsette å redigere) spørsmål én gang først. \n"
            "Kan også være smart å sette publisert=nei før du lagrer."
        )

    changeform_link.short_description = "Alternativer"  # omit column header

    class Meta:
        verbose_name = "testspørsmål"
        verbose_name_plural = "testspørsmål"

    def __str__(self):
        return str(self.text)


def validate_weight_syntax(code):
    try:
        split = code.split(",")
        [int(i) for i in split]
    except Exception:
        raise ValidationError("Kun helltal som vekter!")


class TestQuestionAlternative(models.Model):

    text = models.TextField(blank=False, verbose_name="svaralternativ")

    question = models.ForeignKey(
        "TestQuestion", null=True, on_delete=models.CASCADE, related_name="alternatives"
    )

    target = models.ManyToManyField(
        "TestResult",
        verbose_name="tilsvarende resultat (lagre én gang for å få korrekte resultater)",
        help_text="Velg resultatene dette alternativet svarer til.",
        blank=True,
    )

    weights = models.TextField(
        verbose_name="vektlegging av resultater",
        help_text=(
            "Bestem hvor mye hvert resultat vektlegges ved valg av dette alternativet. "
            "Format er 3,1,4 (altså heltall) det 3 er vekten til det øveste resultatet osv. "
            "Hvis blank får alle vekt 1, og hvis listen ikke er lang nok får resten vekt 1"
        ),
        blank=True,
        validators=[validate_weight_syntax],
    )

    def get_target_with_weights(self):
        split = self.weights.split(",")
        if split == [""]:
            ints = []
        else:
            ints = [int(i) for i in split]
        targets = self.target.all()
        my_list = list(zip(targets, ints))
        if len(ints) < len(targets):
            for i in range(len(ints), len(targets)):
                my_list.append((targets[i], 1))
        return my_list

    class Meta:
        verbose_name = "alternativ"
        verbose_name_plural = "alternativer"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for target in self.target.all():
            if target.test != self.question.test:
                self.target.remove(target)
        super().save(*args, **kwargs)


class TestResult(models.Model):

    title = models.CharField(max_length=100, blank=False)

    content = models.TextField(blank=False, verbose_name="beskrivelse")

    test = models.ForeignKey(
        "Test", null=True, on_delete=models.CASCADE, related_name="results"
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "testresultat"
        verbose_name_plural = "testresultater"
