from django.contrib import admin

# Register your models here.
from .models import Position, Candidate, Vote

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)