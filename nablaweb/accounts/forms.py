from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.models import User
from accounts.models import UserProfile
import subprocess
import settings
class LoginForm(forms.Form):
    username = forms.CharField(label="Brukernavn")
    password = forms.CharField(widget=forms.PasswordInput, label="Passord", required=False)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)



def is_ntnu_username(username):
    """Skjekker om brukernavnet finnes i passwd-fila fra en av ntnus studlinuxservere"""
    try:
        regex = '^%s:' % username
        process = subprocess.Popen(['grep',regex, settings.NTNU_PASSWD], shell=False, stdout=subprocess.PIPE)
        return bool(process.communicate()[0])
    # Hvis ikke settings.NTNU_PASSWD finnes  
    # TODO: Ordne med feilmelding her
    except:
        return False


class RegistrationForm(forms.Form):
    username = forms.CharField(label="NTNU-Brukernavn", required=True)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                raise forms.ValidationError(("Dette brukernavnet er allerede i bruk."))
            else:
                return self.cleaned_data

        except User.DoesNotExist:

            if is_ntnu_username(username):
                return self.cleaned_data
            else:
                raise forms.ValidationError(("Ikke et ntnubrukernavn."))


