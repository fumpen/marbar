from django import forms
from django.contrib.auth.models import User
from management.models import MarBar, Event
from score_board.models import ScoreUnit
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


STD_FORM = [('1A', 1), ('2A', 1), ('3A', 1), ('4A', 1), ('5A', 1), ('6A', 1), ('7A', 1),
            ('1B', 2), ('2B', 2), ('3B', 2), ('4B', 2), ('5B', 2), ('6B', 2), ('7B', 2),
            ('1C', 3), ('2C', 3), ('3C', 3), ('4C', 3), ('5C', 3), ('6C', 3), ('7C', 3),
            ('1D', 4), ('2D', 4), ('3D', 4), ('4D', 4), ('5D', 4), ('6D', 4), ('7D', 4),
            ('Aspirants', 0), ('Crew', 0), ('MarBar Committee', 0)]


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
    #banner = forms.ImageField(required=False)
    users = forms.ModelMultipleChoiceField(queryset=None, to_field_name='username',
                                           widget=forms.CheckboxSelectMultiple, required=False)
    end_date = forms.DateTimeField(widget=forms.DateTimeInput, input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                                                                              '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M'])
    create_standard_fields = forms.BooleanField(required=False)

    intended_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = MarBar
        fields = ['title', 'end_date', 'is_active', 'create_standard_fields']

    def __init__(self, *args, **kwargs):
        user_choices = User.objects.all().exclude(is_superuser=True)
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = user_choices

    def save(self, new_instance=False, update_instance=False):
        if self.is_valid() & new_instance:
            with transaction.atomic():
                new_marbar = MarBar.objects.create(title=self.cleaned_data['title'],
                                                   end_date=self.cleaned_data['end_date'], is_active=False)
                for u in self.cleaned_data['users']:
                    new_marbar.users.add(u)
                new_marbar.save()

                if self.cleaned_data['create_standard_fields']:
                    for n, p in STD_FORM:
                        ScoreUnit.objects.create(title=n, points=0, placement=p, marbar=new_marbar)

        if self.is_valid() & update_instance:
            marbar_update = MarBar.objects.get(pk=self.cleaned_data['intended_pk'])
            with transaction.atomic():
                marbar_update.title = self.cleaned_data['title']
                marbar_update.end_date = self.cleaned_data['end_date']
                marbar_update.users.clear()
                for u in self.cleaned_data['users']:
                    marbar_update.users.add(u)
                marbar_update.save()

                if self.cleaned_data['create_standard_fields']:
                    for n, p in STD_FORM:
                        ScoreUnit.objects.create(title=n, points=0, placement=p, marbar=marbar_update)




class EventForm(forms.Form):
    title = forms.CharField()
    info = forms.CharField(required=False)
    start_date = forms.DateTimeField(widget=forms.DateTimeInput, input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                                                                              '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M'])

    end_date = forms.DateTimeField(widget=forms.DateTimeInput, input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                                                                              '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M'])
    class Meta:
        model = MarBar
        fields = ['title', 'info', 'start_date', 'end_date']

    def save(self, active_marbar):
        if self.is_valid():
            with transaction.atomic():
                new_event = Event(marbar=active_marbar, title=self.cleaned_data['title'],
                                  info=self.cleaned_data['info'], start_date=self.cleaned_data['start_date'],
                                  end_date=self.cleaned_data['end_date'])
                new_event.save()
