from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Position(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_vying = models.DateTimeField()
    end_vying = models.DateTimeField()
    start_voting = models.DateTimeField()
    end_voting = models.DateTimeField()

    def __str__(self):
        return self.title

class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} for {self.position.title}"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.user.username}"
