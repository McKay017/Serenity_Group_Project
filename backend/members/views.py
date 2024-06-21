from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from formtools.wizard.views import SessionWizardView
from .forms import ProposedEmailForm, SeconderForm, GeneralInfoForm, PasswordConfirmForm
from .models import Proposed
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

FORMS = [
    ("step1", ProposedEmailForm),
    ("step2", SeconderForm),
    ("step3", GeneralInfoForm),
    ("step4", PasswordConfirmForm)
]

TEMPLATES = {
    "step1": "step1.html",
    "step2": "step2.html",
    "step3": "step3.html",
    "step4": "step4.html"
}

class UserFormWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]

        # Ensure user is authenticated and retrieve current user
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        
        user = self.request.user
        password = form_data[3].get('password')
        
        # Check if password matches the user's password
        if not user.check_password(password):
            return render(self.request, 'step4.html', {
                'wizard': self,
                'error': 'Incorrect password. Please try again.'
            })

        # Save form data to Proposed model
        try:
            proposed_instance = Proposed.objects.create(
                proposed_email=form_data[0].get('proposed_email'),
                seconder_userid=form_data[1].get('seconder_userid'),
                seconder_email=form_data[1].get('seconder_email'),
                name=form_data[2].get('name'),
                id_number=form_data[2].get('id_number'),
                occupation=form_data[2].get('occupation'),
                employer=form_data[2].get('employer'),
                relationship_status=form_data[2].get('relationship_status'),
                children=form_data[2].get('children'),
                phone_number=form_data[2].get('phone_number'),
                salary_range=form_data[2].get('salary_range'),
                user=user,  # Save the current user who submitted the form
                email=user.email  # Save the email of the current user
            )

            # Send email to seconder_email
            context = {
                'proposed_email': form_data[0].get('proposed_email'),
                'seconder_userid': form_data[1].get('seconder_userid'),
                'seconder_email': form_data[1].get('seconder_email'),
                'name': form_data[2].get('name'),
                'id_number': form_data[2].get('id_number'),
                'occupation': form_data[2].get('occupation'),
                'employer': form_data[2].get('employer'),
                'relationship_status': form_data[2].get('relationship_status'),
                'children': form_data[2].get('children'),
                'phone_number': form_data[2].get('phone_number'),
                'salary_range': form_data[2].get('salary_range'),
                'user' : form_data[2].get('user'),
            }

            email_subject = 'Serenity Country Club'
            email_body = render_to_string('email.html', context)
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [form_data[1].get('seconder_email')]
            )
            email.content_subtype = 'html'  # Set the email content type to HTML
            email.send()

            # Render the 'done' template with form data
            return render(self.request, 'done.html', {'form_data': form_data})

        except ValidationError as e:
            return render(self.request, 'step4.html', {
                'wizard': self,
                'error': e.message
            })


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Proposed, Accepted, Rejected

def display_requests(request, userid):
    # Fetch all proposed requests for the given userid
    proposed_requests = Proposed.objects.filter(seconder_userid=userid)

   

    

    return render(request, 'display_requests.html', {'proposed_requests': proposed_requests})

def handle_notification(request, proposed_id, action):
    proposed_request = get_object_or_404(Proposed, pk=proposed_id)

    

    if action == 'accept':
        # Create a record in Accepted table
        Accepted.objects.create(
            proposed_email=proposed_request.proposed_email,
            seconder_userid=proposed_request.seconder_userid,
            seconder_email=proposed_request.seconder_email,
            name=proposed_request.name,
            id_number=proposed_request.id_number,
            occupation=proposed_request.occupation,
            employer=proposed_request.employer,
            relationship_status=proposed_request.relationship_status,
            children=proposed_request.children,
            phone_number=proposed_request.phone_number,
            salary_range=proposed_request.salary_range,
            user=proposed_request.user,
            email=proposed_request.user.email
        )

        # Send registration link email to proposed_email
        registration_link = "http://example.com/registration"  # Replace with actual registration link
        subject = 'Registration Link'
        message = render_to_string('registemail.html', {'registration_link': registration_link})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [proposed_request.proposed_email])

    elif action == 'decline':
        # Create a record in Rejected table
        Rejected.objects.create(
            proposed_email=proposed_request.proposed_email,
            seconder_userid=proposed_request.seconder_userid,
            seconder_email=proposed_request.seconder_email,
            name=proposed_request.name,
            id_number=proposed_request.id_number,
            occupation=proposed_request.occupation,
            employer=proposed_request.employer,
            relationship_status=proposed_request.relationship_status,
            children=proposed_request.children,
            phone_number=proposed_request.phone_number,
            salary_range=proposed_request.salary_range,
            user=proposed_request.user,
            email=proposed_request.user.email
        )

    # Delete the proposed request after processing
    proposed_request.delete()

    return redirect('display_requests', userid=proposed_request.seconder_userid)

