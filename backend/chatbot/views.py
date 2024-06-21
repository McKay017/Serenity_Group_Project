from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import FAQ
from .forms import QuestionForm
from django.db.models import Q

def chatbot_view(request):
    response = None
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            user_question = form.cleaned_data['question']
            # Basic matching using case insensitive containment
            faqs = FAQ.objects.filter(Q(question__icontains=user_question))
            if faqs.exists():
                response = faqs.first().answer
            else:
                response = "Sorry, I don't know the answer to that question."
    else:
        form = QuestionForm()

    return render(request, 'chatbot.html', {'form': form, 'response': response})
