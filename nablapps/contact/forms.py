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
    start_time = forms.CharField(
        label="Start tidspunkt:", max_length=100, required=True
    )
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
            + "Start tidspunkt: "
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


class ForCompanyForm(forms.Form):
    company = forms.CharField(label="Bedrift:", max_length=100, required=True)
    contact_person = forms.CharField(
        label="Kontaktperson:", max_length=100, required=True
    )
    email = forms.CharField(label="Epost:", required=True)
    purpose = forms.CharField(label="Kommentar:", widget=forms.Textarea, required=True)

    def process(self):
        cd = self.cleaned_data
        company = cd["company"]
        email = cd["email"]
        purpose = "Formål: " + cd["purpose"]
        return company, purpose, email


class ContactForm(forms.Form):
    reciever_choices = (
        ("Styret", "Styret"),
        ("PostKom", "PostKom"),
        ("ITV ved IFY", "ITV ved IFY"),
        ("ITV ved IMF", "ITV ved IMF"),
        ("BedKom", "BedKom"),
    )

    your_name = forms.CharField(label="Ditt navn:", max_length=100, required=False)
    reciever = forms.ChoiceField(choices=reciever_choices, label="Mottaker")
    subject = forms.CharField(label="Emne:", max_length=100, required=True)
    message = forms.CharField(label="Melding:", widget=forms.Textarea, required=True)
    email = forms.EmailField(label="Din e-post:", max_length=100, required=False)
    spam_check = forms.FloatField(max_value=20, required=True)
    right_answer = forms.FloatField(
        max_value=20, required=True, widget=forms.HiddenInput()
    )

    def process(self):
        cd = self.cleaned_data
        subject = cd["subject"]
        if cd["your_name"]:
            message = cd["message"] + "\n-" + cd["your_name"]
        else:
            message = cd["message"] + "\n-" + "Anonym"
        email = cd["email"]
        return subject, message, email

    def get_reciever(self):
        cd = self.cleaned_data
        reciever = cd["reciever"]
        return reciever

    def get_answer(self):
        cd = self.cleaned_data
        answer = cd["spam_check"]
        return answer

    def get_right_answer(self):
        cd = self.cleaned_data
        right_answer = cd["right_answer"]
        return right_answer
