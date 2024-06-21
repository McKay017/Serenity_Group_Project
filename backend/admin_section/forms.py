from django import forms
from .models import Category , Product , UserProfile , Waiter ,Room
from django.contrib.auth.forms import AuthenticationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'contents', 'price']

class RegistrationForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    RELATIONSHIP_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender', widget=forms.Select(attrs={'class': 'form-control'}))
    relationship_status = forms.ChoiceField(choices=RELATIONSHIP_CHOICES, label='Relationship Status', widget=forms.Select(attrs={'class': 'form-control'}))
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['full_name', 'gender', 'dob', 'national_id', 'email', 'occupation', 'employer', 'relationship_status', 'phone_number', 'agreed_to_rules', 'agreed_to_waiver']
        

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.groups.filter(name='member').exists():
            raise forms.ValidationError("This account does not belong to the 'members' group.", code='invalid_login')


class WaiterForm(forms.ModelForm):
    class Meta:
        model = Waiter
        fields = ['full_name', 'date_of_birth', 'gender', 'contact', 'home_address', 'email', 'waiter_id']

from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['name', 'image']

from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'room_type', 'image', 'price_per_night']


from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'member_name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms

class MpesaTransactionForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)



from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email...'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message...'}),
        }