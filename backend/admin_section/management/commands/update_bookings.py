# update_bookings.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from admin_section.models import Room, Booking

class Command(BaseCommand):
    help = 'Update room booking statuses'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        expired_bookings = Booking.objects.filter(end_date__lt=today)
        for booking in expired_bookings:
            room = Room.objects.get(pk=booking.room.id)
            room.is_booked = False
            room.save()
            booking.delete()
        self.stdout.write(self.style.SUCCESS('Bookings updated successfully'))
