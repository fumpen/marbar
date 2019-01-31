from django import forms
from django.contrib.auth.models import User

class NewUser(forms.Form):
    title = forms.CharField(max_length=100)
    mail = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    def clean_user(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 == pass2:
            return cleaned_data
        else:
            forms.ValidationError('The provided passwords must be the same')




class MarBarForm(forms.Form):
    title = forms.CharField()
    banner = forms.ImageField()
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), to_field_name='username', widget=forms.CheckboxSelectMultiple) #widget=forms.Select(attrs={'username': 'username'}) -- widget=forms.widgets.RadioSelect
    end_date = forms.DateTimeField()
    is_active = forms.BooleanField()


    def __init__(self, *args, **kwargs):

        user_choices = kwargs.pop('user_choices')
        #user_choices = [(x.username, x.id) for x in user_choices]

        super().__init__(*args, **kwargs)

        self.fields['users'].queryset = user_choices
