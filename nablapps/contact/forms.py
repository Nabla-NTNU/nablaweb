from django import forms

class ContactForm(forms.Form):
    your_name = forms.CharField(label='Ditt navn', max_length=100, required=True)
    email = forms.EmailField(label='Din e-post:', max_length=100, required=True)
    subject = forms.CharField(label='Emne', max_length=100)
    message = forms.CharField(label='Melding', widget=forms.Textarea, required=True)
    spam_check = forms.FloatField(label='svar', max_value=20, required=True)

    test_val = 0

    your_name_val = ''
    email_val = ''
    subject_val = ''
    message_val = ''

    def process(self):
        cd = self.cleaned_data
        subject = cd['subject']
        message = cd['message']+'\n-'+ cd['your_name']
        email = cd['email']
        return subject, message, email

    def get_answer(self):
        cd = self.cleaned_data
        answer = cd['spam_check']
        return answer

    def get_test_val(self):
        test_val = self.test_val
        return test_val

