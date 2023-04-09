from django import forms
from .models import my_fields,my_types
from multiselectfield import MultiSelectFormField

#signup and signin forms.
class signup_form(forms.Form):
    username = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'placeholder':'Username','class': 'sign'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Email','class': 'sign'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value = True,attrs={'placeholder':'Password','class': 'sign'}))
    confirm_pass = forms.CharField(widget=forms.PasswordInput(render_value = True,attrs={'placeholder':'Confirm Password','class': 'sign'}))

class signin_form(forms.Form):
    username = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'placeholder':'Username','class': 'sign'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value = True,attrs={'placeholder':'Password','class': 'sign'}))

#form to share opportunity.
class share_form(forms.Form):
    head = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Title','class': 'share'}))
    desc = forms.CharField( widget=forms.Textarea(attrs={'placeholder': 'Brief Description', 'class': 'share'}))
    start = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','class': 'date'}))
    end = forms.DateField(required = False,widget=forms.TextInput(attrs={'type': 'date','class':'date'}))
    location = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Location','class': 'share'}))
    details = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'More Details about the activity','class': 'share'}))
    image = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Provide link for any related image','class': 'share'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Official link of opportunity','class': 'share'}))
    type = forms.ChoiceField(choices=my_types, widget=forms.Select(attrs={'placeholder': 'Category','class': 'share'}))
    interest = MultiSelectFormField(choices = my_fields, widget=forms.CheckboxSelectMultiple(attrs={'placeholder': 'Interest tags','id': 'interest'}))

#form to subscribe to the mail notfications.
class mails_form(forms.Form):
    fields = MultiSelectFormField(required=False,choices = my_fields, widget=forms.CheckboxSelectMultiple(attrs={'placeholder': 'Field tags','id': 'interest'}))
    mail_id = forms.EmailField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Email ID','class': 'share'}))
    unsubscribe = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'placeholder': 'Unsubscribe','class': 'share'}))
   
class validate_form(forms.Form):
    mail_id = forms.EmailField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Email ID','class': 'share'}))
