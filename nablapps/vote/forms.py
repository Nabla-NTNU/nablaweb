from django.forms import BaseInlineFormSet, ModelForm
from django.forms.models import inlineformset_factory

from .models import Alternative, BallotContainer, BallotEntry, Voting

# For adding/editing alternatives (admin)
AlternativeFormset = inlineformset_factory(
    Voting, Alternative, fields=("text",), can_delete=False, extra=10
)

# class CustomInlineFormset(BaseInlineFormSet):
#    def clean(self):
#        super().clean()
#        # Validation of the formset
#
#        ballot = {}
#        for form in self.forms:
#            # Validation, etc
#            pass

# class BallotForm(ModelForm):
#    class Meta:
#        model = BallotContainer
#        fields = (
#            "voting",
#        )

# For submitting vote Ballot
# PrioritizedAlternativesFormset = inlineformset_factory(
#        BallotContainer, BallotEntry, fields=("alternative",), can_delete=False
# )
