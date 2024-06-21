from django.urls import path
from .views import UserFormWizard, FORMS
from .views import *

urlpatterns = [
    path('wizard/', UserFormWizard.as_view(FORMS), name='user_form_wizard'),
    # other paths...

    path('requests/<str:userid>/', display_requests, name='display_requests'),
    path('handle-notification/<int:proposed_id>/<str:action>/', handle_notification, name='handle_notification'),
]

