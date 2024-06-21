from django import forms

class ProposedEmailForm(forms.Form):
    proposed_email = forms.EmailField(label='Proposed Email')

class SeconderForm(forms.Form):
    seconder_userid = forms.CharField(label='Seconder UserID', max_length=100)
    seconder_email = forms.EmailField(label='Seconder Email')

class GeneralInfoForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    id_number = forms.CharField(label='ID Number', max_length=100)
    occupation = forms.CharField(label='Occupation', max_length=100)
    employer = forms.CharField(label='Employer', max_length=100)
    relationship_status = forms.CharField(label='Relationship Status', max_length=50)
    children = forms.CharField(label='Children', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    salary_range = forms.CharField(label='Salary Range', max_length=100)

class PasswordConfirmForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
