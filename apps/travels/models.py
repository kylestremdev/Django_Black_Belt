from __future__ import unicode_literals

from django.db import models

from ..users.models import User

from datetime import date, datetime

# Create your models here.
class TripManager(models.Manager):
    def add_trip(self, post_data):
        errors = []
        empty_date = False

        #destination
        if len(post_data['destination']) < 1:
            errors.append("Destination cannot be empty")
        #description
        if len(post_data['description']) < 1:
            errors.append("Description cannot be empty")
        #start date (Travel date from) blank
        if len(post_data['start_date']) < 1:
            errors.append("Travel Date From cannot be empty")
            empty_date = True

        #end date (Travel date to) blank
        if len(post_data['start_date']) < 1:
            errors.append("Travel Date From cannot be empty")
            empty_date = True

        #validate dates
        if not empty_date:
            now = datetime.now()
            start_date = datetime.strptime(post_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(post_data['end_date'], '%Y-%m-%d')

            if start_date < now:
                errors.append("Travel Date From must be in the future")

            if end_date < start_date:
                errors.append("Travel Date To must be after Travel Date From")

        if len(errors) > 0:
            return errors

        user = User.objects.get(id=post_data['user_id'])

        Trip.objects.create(
            planned_by=user,
            destination=post_data['destination'],
            description=post_data['description'],
            start_date=start_date.date(),
            end_date=end_date.date()
        )

        return None

class Trip(models.Model):
    planned_by = models.ForeignKey(User, related_name="trips")
    joined_users = models.ManyToManyField(User, related_name="joined_trips")
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
