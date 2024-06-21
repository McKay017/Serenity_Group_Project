from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Position, Candidate, Vote
from .forms import CandidateForm, VoteForm

@login_required
def positions_list(request):
    positions = Position.objects.all()
    return render(request, 'positions_list.html', {'positions': positions})

@login_required
def vie_for_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    if timezone.now() < position.start_vying or timezone.now() > position.end_vying:
        messages.error(request, 'Vying period is not active.')
        return redirect('positions_list')
    if Candidate.objects.filter(user=request.user, position=position).exists():
        messages.error(request, 'You have already vied for this position.')
        return redirect('positions_list')
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.position = position
            candidate.save()
            messages.success(request, 'You have successfully vied for the position.')
            return redirect('positions_list')
    else:
        form = CandidateForm()
    return render(request, 'vie_for_position.html', {'position': position, 'form': form})

@login_required
def vote(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    if timezone.now() < position.start_voting or timezone.now() > position.end_voting:
        messages.error(request, 'Voting period is not active.')
        return redirect('positions_list')
    if Vote.objects.filter(voter=request.user, candidate__position=position).exists():
        messages.error(request, 'You have already voted for this position.')
        return redirect('positions_list')
    candidates = Candidate.objects.filter(position=position)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.voter = request.user
            vote.save()
            messages.success(request, 'Your vote has been cast.')
            return redirect('positions_list')
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'position': position, 'candidates': candidates, 'form': form})

@login_required
def results(request):
    positions = Position.objects.all()
    results = {}
    for position in positions:
        candidates = Candidate.objects.filter(position=position)
        winner = max(candidates, key=lambda c: Vote.objects.filter(candidate=c).count(), default=None)
        if winner:
            results[position] = winner
    return render(request, 'results.html', {'results': results})
