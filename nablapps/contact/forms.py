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


class ContactForm(forms.Form):
    reciever_choices = (
        ("Styret", "Styret"),
        ("PostKom", "PostKom"),
        ("ITV ved IFY", "ITV ved IFY"),
        ("ITV ved IMF", "ITV ved IMF"),
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
