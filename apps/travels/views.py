from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Trip
from ..users.models import User
# Create your views here.
def index(request):
    context = {
        'user_trips': User.objects.get(id=request.session['user']['id']).trips.all()|Trip.objects.filter(joined_users__id=request.session['user']['id']).order_by('start_date'),
        'other_trips': Trip.objects.exclude(planned_by__id=request.session['user']['id']).exclude(joined_users__id=request.session['user']['id'])
    }

    return render(request, 'travels/index.html', context)

def add(request):
    return render(request, 'travels/add.html')

def create_trip(request):
    if request.method == "POST":

        response = Trip.objects.add_trip(request.POST)

        if type(response) is list:
            for error in response:
                messages.error(request, error)
            return redirect(reverse('travels:add'))

        return redirect(reverse('travels:index'))


def join_trip(request, trip_id, user_id):
    trip = Trip.objects.get(id=trip_id)
    user = None
    try:
        user = User.objects.get(id=user_id)
    except:
        messages.error(request, "User does not exist")
        return redirect(reverse('travels:index'))

    if request.session['user']['id'] == user_id:
        messages.error(request, 'Cannot join your own trip')
        return redirect(reverse('travels:index'))
    try:
        if trip.joined_users.get(id=user_id):
            messages.error(request, 'User has already joined this trip')
            return redirect(reverse('travels:show_trip', kwargs={'trip_id':trip_id}))
    except:
        trip.joined_users.add(user)
        return redirect(reverse('travels:show_trip', kwargs={'trip_id':trip_id}))

def show_trip(request, trip_id):
    context = {}

    try:
        context['trip'] = Trip.objects.get(id=trip_id)
    except:
        messages.error(request, "Trip does not exist")
        return redirect(reverse('travels:index'))

    return render(request, 'travels/show.html', context)
