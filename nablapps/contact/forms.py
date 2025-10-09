from django import forms

# Two almost identical forms, should perhaps rather make an abstract class with common fields.


class FeedbackForm(forms.Form):
    your_name = forms.CharField(label="Ditt navn:", max_length=100, required=False)
    subject = forms.CharField(label="Emne:", max_length=100, required=False)
    message = forms.CharField(label="Melding:", widget=forms.Textarea, required=True)
    email = forms.EmailField(label="Din e-post:", max_length=100, required=False)
    spam_check = forms.FloatField(max_value=20, required=True)
    right_answer = forms.FloatField(
        max_value=20, required=True, widget=forms.HiddenInput()
    )

    def process(self):
        cd = self.cleaned_data
        subject = cd["subject"]
        message = cd["message"] + "\n-" + cd["your_name"]
        email = cd["email"]
        return subject, message, email

    def get_answer(self):
        cd = self.cleaned_data
        answer = cd["spam_check"]
        return answer

    def get_right_answer(self):
        cd = self.cleaned_data
        right_answer = cd["right_answer"]
        return right_answer


# Utrolig Wack og dårlig løsning - altså er kok av klassen over - bør finne på noe bedre!
class RoomForm(forms.Form):
    your_name = forms.CharField(label="Ditt navn:", max_length=100, required=False)
    committee_name = forms.CharField(label="Komite:", max_length=100, required=False)
    date = forms.CharField(label="Dato:", required=True)
    start_time = forms.CharField(label="Starttidspunkt:", max_length=100, required=True)
    duration = forms.CharField(label="Varighet:", max_length=100, required=True)
    num_people = forms.IntegerField(
        label="Estimert antall:", max_value=400, required=False
    )
    purpose = forms.CharField(
        label="Kort beskrivelse av formål:", widget=forms.Textarea, required=True
    )
    email = forms.EmailField(label="Din e-post:", max_length=100, required=True)
    spam_check = forms.FloatField(max_value=20, required=True)
    right_answer = forms.FloatField(
        max_value=20, required=True, widget=forms.HiddenInput()
    )

    def process(self):
        cd = self.cleaned_data
        committee_name = cd["committee_name"]
        email = cd["email"]
        purpose = (
            "Navn: "
            + cd["your_name"]
            + "\n"
            + "Komite: "
            + cd["committee_name"]
            + "\n"
            + "Dato: "
            + cd["date"]
            + "\n"
            + "Starttidspunkt: "
            + cd["start_time"]
            + "\n"
            + "Varighet: "
            + cd["duration"]
            + "\n"
            + "Estimert antall: "
            + str(cd["num_people"])
            + "\n"
            + "Formål: "
            + cd["purpose"]
        )
        return committee_name, purpose, email

    def get_answer(self):
        cd = self.cleaned_data
        answer = cd["spam_check"]
        return answer

    def get_right_answer(self):
        cd = self.cleaned_data
        right_answer = cd["right_answer"]
        return right_answer


class UtstyrForm(forms.Form):
    utstyr_tilgjengelig = [
        ("Laavo", "Lavvo 8-10 personer"),
        ("Kubb", "Kubb"),
        ("Liggeunderlag", "Liggeunderlag (3)"),
        ("Tarp", "Tarp"),
        ("Hengekøye", "Hengekøye (3)"),
        ("Stormkjøkken", "Stormkjøkken"),
        ("sitteunderlag", "Sitteunderlag (10)"),
        ("liten tursag", "Liten tursag"),
    ]

    your_name = forms.CharField(label="Ditt navn:", max_length=100, required=False)
    equipment = forms.ChoiceField(
        label="Utstyr", choices=utstyr_tilgjengelig, required=True
    )
    start_date = forms.CharField(label="Startdato:", required=True)
    end_date = forms.CharField(label="Sluttdato:", max_length=100, required=True)
    comment = forms.CharField(label="Kommentar:", widget=forms.Textarea, required=False)
    email = forms.EmailField(label="Din e-post:", max_length=100, required=True)
    spam_check = forms.FloatField(max_value=20, required=True)
    right_answer = forms.FloatField(
        max_value=20, required=True, widget=forms.HiddenInput()
    )

    def process(self):
        cd = self.cleaned_data
        email = cd["email"]
        subject = "Utstyrbooking av " + cd["equipment"]
        purpose = (
            "Navn: "
            + cd["your_name"]
            + "\n"
            + "\n"
            + "Ønsker å låne: "
            + cd["equipment"]
            + "\n"
            + "Startdato: "
            + cd["start_date"]
            + "\n"
            + "Sluttdato: "
            + cd["end_date"]
            + "\n"
            + cd["comment"]
        )
        return subject, purpose, email

    def get_answer(self):
        cd = self.cleaned_data
        answer = cd["spam_check"]
        return answer

    def get_right_answer(self):
        cd = self.cleaned_data
        right_answer = cd["right_answer"]
        return right_answer
