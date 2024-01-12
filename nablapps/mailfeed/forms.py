from django import forms


class MailFeedForm(forms.Form):
    name_field = forms.CharField(required=True)

    def get_name(self) -> str:
        cd = self.cleaned_data
        name = cd["name_field"]
        return name


class SubscribeForm(forms.Form):
    email_field = forms.EmailField(widget=forms.EmailInput)

    def get_email(self) -> str:
        cd = self.cleaned_data
        email = cd["email_field"]
        return email


class UnsubscribeForm(forms.Form):
    checkbox_field = forms.BooleanField()

    def get_result(self) -> bool:
        cd = self.cleaned_data
        result = cd["checkbox_field"]
        return result


class EmailForm(forms.Form):
    subject_field = forms.CharField(max_length=80)
    content_field = forms.CharField(required=True, widget=forms.Textarea)

    def get_subject(self) -> str:
        cd = self.cleaned_data
        subject = cd["subject_field"]
        return subject

    def get_content(self) -> str:
        cd = self.cleaned_data
        content = cd["content_field"]
        return content
