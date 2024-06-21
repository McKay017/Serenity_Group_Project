
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect ,HttpResponse
from .forms import CategoryForm  # Import the form
from django.shortcuts import render, redirect
from .forms import *
from .models import *  # Import the model
from .forms import ProductForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import UserProfile
import random
import string
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Product




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_staff and user.is_superuser:
                login(request, user)
                return redirect('home')  # Redirect to home page on success
            else:
                form.add_error(None, 'Invalid credentials or not a superuser')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    user = request.user
    members_group = Group.objects.get(name='member')
    waiters_group = Group.objects.get(name='Waiters')
    food = Product.objects.all().count
    
    members_count = members_group.user_set.count()
    waiters_count = waiters_group.user_set.count()
    context = {
        'username': user.username,
        'members_count' : members_count,
        'waiters_count' : waiters_count,
        'date_joined': user.date_joined,
        'food' : food
    }
    return render(request,'adminhome.html',context)

@login_required
def addfoodmenu(request):
    user = request.user
    categories = Category.objects.prefetch_related('product_set').all()
    context = {
        'categories' : categories,
        'username': user.username,
    }
    return render(request,'adminmenu.html',context)

@login_required
def addroomadmin(request):
    user = request.user
    rooms = Room.objects.all()
    context = {
        'username': user.username,
        'rooms' : rooms
    }
    return render(request,'adminroom.html',context)

@login_required
def landingpage(request):
    user = request.user
    context = {
        'username': user.username,
    }
    return render(request,'adminwebsite.html',context)

@login_required
def adminmemberspage(request):
    user = request.user
    members_group = Group.objects.get(name='member')
    
    # Get all users in the 'members' group
    members = User.objects.filter(groups=members_group)
    context = {
        'username': user.username,
        'members' : members,
    }
    return render(request,'adminmembers.html',context)

@login_required
def adminwaiterspage(request):
    user = request.user
    waiters_group = Group.objects.get(name='Waiters')
    
    # Get all users in the 'members' group
    waiters = User.objects.filter(groups=waiters_group)
    context = {
        'username': user.username,
        'waiters' : waiters
    }
    return render(request,'adminwaiter.html',context)

def category_input(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()  # Save the form data to the database
            # You can access the saved category object using 'category'
            return redirect('menu_category')  # Redirect to success page
    else:
        form = CategoryForm()
    return render(request, 'admincategory.html', {'form': form})

from .forms import RegistrationForm



def generate_unique_id():
    letters = string.ascii_uppercase
    while True:
        digits = ''.join(random.choices(string.digits, k=4))
        unique_id = ''.join(random.choices(letters, k=2)) + digits
        if not User.objects.filter(username=unique_id).exists():
            break
    return unique_id

def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

def send_registration_email(user,otp):
    subject = 'Registration Successful'
    html_message = render_to_string('registration_email.html', {'user': user,'otp':otp})
    plain_message = strip_tags(html_message)
    from_email = 'your@example.com'  # Replace with your email
    to_email = user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


def generate_and_register_user(email):
    # Check if a user with this email already exists
    if not User.objects.filter(email=email).exists():
        try:
            profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            # Handle the case where the profile with the provided email does not exist
            return None
        
        # Create a new user with the email
        unique_id = generate_unique_id()
        otp = generate_otp()
        print(otp)
        user = User.objects.create_user(unique_id, email, otp)
        
        # Optionally, you can set additional fields for the user
        member_group, _ = Group.objects.get_or_create(name='member')
        user.groups.add(member_group)
        
        user.save()
        
        # Generate and set unique ID and OTP for the user's profile
        send_registration_email(user,otp)       
        return user
    else:
        # User with this email already exists, handle accordingly
        return None



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Call the function to generate and register the user
            generate_and_register_user(form.cleaned_data['email'])
            return redirect('registration_success')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_product')  # You need to define 'success_url' in your urls.py
    else:
        form = ProductForm()
    return render(request, 'adminfoodmenu.html', {'form': form})

#def register(request):
#    if request.method == 'POST':
#       form = RegistrationForm(request.POST)
#       if form.is_valid():

 #           user_id = ''.join(random.choices('0123456789', k=8))
  #          user_password = ''.join(random.choices('0123456789', k=4))
   #         user = User.objects.create_user(username=user_id, password=user_password)
    #        
     #       # Create user profile data
      #      user_profile = form.save(commit=False)
       #     user_profile.user = user
        #    user_profile.save()
#
 #           # Send email
  #          send_registration_email(user_profile.email, user_id, user_password)
   #         return redirect('registration_success')
    #else:
     #   form = RegistrationForm()
    #return render(request, 'register.html', {'form': form})


def registration_success(request):
    return render(request, 'success.html')

def homepage(request):
    return render(request,'home.html')

def dine(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request,'dine.html',context)

def room(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request,'rooms.html',context)

def logout_view(request):
    logout(request)
    return redirect('login_page')  # Redirect to login page or any other page



class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'member_login.html'

    def get_success_url(self):
        return '/member_home/'
    
def member_logout(request):
    logout(request)
    return redirect('CustomLoginView') 

from .forms import WaiterForm

def member_home(request):
    user = request.user
    context = {
        'username' : user.username,
        'date_joined' : user.date_joined
    }
    return render(request,'memberdashboard.html' ,context)

def generate_unique_id():
    while True:
        new_id = f'WAT{random.randint(100, 999)}'
        if not Waiter.objects.filter(waiter_id=new_id).exists():
            return new_id

def generate_random_password():
    return ''.join(random.choices(string.digits, k=4))

def register_waiter(request):
    if request.method == 'POST':
        waiter_form = WaiterForm(request.POST)
        if waiter_form.is_valid():
            waiter_data = waiter_form.cleaned_data
            waiter_id = generate_unique_id()
            password = generate_random_password()
            
            # Create the User instance
            user = User.objects.create_user(
                username=waiter_id,
                email=waiter_data['email'],
                password=password,
                first_name=waiter_data['full_name'].split()[0],
                last_name=' '.join(waiter_data['full_name'].split()[1:])
            )

            # Create the Waiter instance
            waiter = waiter_form.save(commit=False)
            waiter.user = user
            waiter.waiter_id = waiter_id
            waiter.save()

            # Add user to the "Waiters" group
            waiters_group = Group.objects.get(name='Waiters')
            waiters_group.user_set.add(user)

            # Send email with login information
            subject = 'Your Waiter Registration Details'
            message = (f'Hello {waiter.full_name},\n\n'
                       f'Your account has been created successfully. Here are your login details:\n'
                       f'Username: {waiter_id}\n'
                       f'Password: {password}\n\n'
                       'Please use these details to log in.')
            from_email = 'newtonzuki7440@gmail.com'
            recipient_list = [waiter.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('waiter_success')
    else:
        waiter_form = WaiterForm()
    return render(request, 'reg_waiter.html', {'waiter_form': waiter_form})

def waiter_success(request):
    return render(request, 'waiters_success.html')


from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_success')
    else:
        form = ImageUploadForm()
    return render(request, 'adminuploadmenuimage.html', {'form': form})

def image_success(request):
    return render(request, 'image_success.html')

from .forms import EmailForm
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

def send_registration_link(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            registration_link = request.build_absolute_uri(reverse('register'))  # Assuming 'register' is the name of your registration URL
            send_mail(
                'Registration Link',
                f'Click the link to register as a member for serenity country club: {registration_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Registration link sent!')
            return redirect('send_registration_link')
    else:
        form = EmailForm()
    
    return render(request, 'send_registration_link.html', {'form': form})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_room')  # Redirect to a success page
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})


def waiter_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name='Waiters').exists():
                login(request, user)
                return redirect('waiter_home')  # redirect to a waiter-specific dashboard
            else:
                messages.error(request, 'You are not authorized to log in as a waiter.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'waiter_login.html')

def waiter_home(request):
    user = request.user
    context = {
        'username' : user.username,
        'date_joined' : user.date_joined
    }
    return render(request,"waiter_dashboard.html",context)

def waiter_leaderboard(request):
    return render(request,"waiter_leaderboard.html")

def waiter_order(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request,"waiter_order.html",context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # For simplicity, using session to store cart items
    cart = request.session.get('cart', [])
    cart.append(product.id)
    request.session['cart'] = cart
    return redirect('dine')

def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    context = {
        'products': products,
    }
    return render(request, 'checkout.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category_list.html', context)


from django.shortcuts import render, get_object_or_404, redirect

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'room_detail.html', {'room': room})

def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create a new booking object but don't save it yet
            new_booking = form.save(commit=False)

            # Optionally, perform additional validation or data processing here

            # Save the booking object to the database
            new_booking.save()

            # Redirect to a success page or another view after successful booking
            return redirect('booking_success')  # Replace with your URL name for success page
    else:
        # Handle GET request (initial form load) here
        form = BookingForm()

    # Render the booking form template with the form object
    return render(request, 'book_room.html', {'form': form})

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

import logging
from .forms import MpesaTransactionForm
from .utils import lipa_na_mpesa_online
from .models import MpesaTransaction

logger = logging.getLogger(__name__)

class MpesaStkPushView(View):
    def get(self, request, *args, **kwargs):
        form = MpesaTransactionForm()
        return render(request, 'mpesa_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MpesaTransactionForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']
            account_reference = "account_ref"
            transaction_desc = "Payment Description"
            callback_url = "https://mydomain.com/path"

            # Ensure phone number is in E.164 format (without leading zeros)
            phone_number = phone_number.replace('+', '').replace(' ', '')
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]

            try:
                response = lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc, callback_url)
                logger.debug(f'M-Pesa API Response: {response}')
                transaction_id = response.get('CheckoutRequestID', '')
                status = response.get('ResponseDescription', 'Transaction Failed')

                if not transaction_id:
                    logger.error(f'Transaction Failed: {response}')
                    return redirect('transaction_failure')

                MpesaTransaction.objects.create(
                    phone_number=phone_number,
                    amount=amount,
                    transaction_id=transaction_id,
                    status=status
                )

                if response.get('ResponseCode') == '0':
                    return redirect('transaction_success')
                else:
                    logger.error(f'Transaction Failed: {response}')
                    return redirect('transaction_failure')
            except Exception as e:
                logger.error(f'Exception during transaction: {e}')
                return redirect('transaction_failure')

        return render(request, 'mpesa_form.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.save()
        return redirect('addfoodmenu')
    return render(request, 'edit_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('addfoodmenu')
    return render(request, 'delete_product.html', {'product': product})


# membership/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Membership
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt

# M-Pesa API credentials (replace with your own)
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
shortcode = 'YOUR_SHORTCODE'
lipa_na_mpesa_online_passkey = 'YOUR_PASSKEY'

def get_mpesa_access_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()['access_token']

def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc):
    access_token = get_mpesa_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": lipa_na_mpesa_online_passkey,
        "Timestamp": "20230614120100",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://your-callback-url.com/callback",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@csrf_exempt
def pay(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['user_id']
        phone_number = data['phone_number']
        membership_type = data['membership_type']
        
        # Determine the amount based on membership type
        if membership_type == 'basic':
            amount = 1.0
        elif membership_type == 'premium':
            amount = 2.0
        elif membership_type == 'vip':
            amount = 3.0
        else:
            return JsonResponse({"error": "Invalid membership type"}, status=400)
        
        # Save membership details
        membership = Membership(user_id=user_id, phone_number=phone_number, membership_type=membership_type)
        membership.save()

        # Initiate M-Pesa payment
        response = lipa_na_mpesa_online(phone_number, amount, "Membership Payment", "Payment for membership")
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process the callback data
        # Update the membership status based on the transaction status
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def landing_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing_page')  # Redirect to a success page or a thank you page
    else:
        form = ContactForm()
    
    return render(request, 'landingpage.html', {'form': form})

def gallery(request):
    return render(request,'gallery.html')

def logins(request):
    return render(request,'logins.html')