from django.shortcuts import render,redirect,get_object_or_404
from .forms import BookingForm
from accounts.models import FreelancerProfile
from services.models import Service
from django.contrib.auth.decorators import login_required
from accounts.views import dashboard
# Create your views here.
from services.models import Service
from accounts.models import Notification
from .models import Booking,Review
from .forms import ReviewForm
from accounts.models import FreelancerProfile,Notification
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import Notification
from django.db.models import Avg
def home(request):
    services = Service.objects.all()

    unread_count = 0
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return render(request, 'home.html', {
        'services': services,
        'unread_count': unread_count
    })



# 🔹 Show all services


# 🔹 Show freelancers for a service
def freelancer_list(request, service_id):
    freelancers = FreelancerProfile.objects.filter(services=service_id)
    return render(request, 'freelancers.html', {'freelancers': freelancers})


# 🔹 Booking form




@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    # ✅ freelancers for this service
    freelancers = FreelancerProfile.objects.filter(services=service)

    form = BookingForm(request.POST or None)

    # ✅ restrict dropdown freelancers
    form.fields['freelancer'].queryset = User.objects.filter(
        freelancerprofile__services=service
    )

    if form.is_valid():
        booking = form.save(commit=False)

        freelancer_id = form.cleaned_data['freelancer']
        freelancer = freelancer_id

        booking.client = request.user
        booking.freelancer = freelancer
        booking.service = service
        booking.status = 'pending'

        booking.save()

        # 🔔 notification
        Notification.objects.create(
            user=freelancer,
            message=f"New booking from {request.user.username} for {service.name}"
        )

        return redirect('dashboard')

    return render(request, 'booking_form.html', {
        'form': form,
        'service': service,
        'freelancers': freelancers
    })

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # only client allowed
    if request.user != booking.client:
        return redirect('dashboard')

    # must be completed
    if booking.status != 'completed':
        return redirect('dashboard')

    # prevent duplicate review
    if Review.objects.filter(booking=booking).exists():
        return redirect('dashboard')

    form = ReviewForm(request.POST or None)

    if form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.client = request.user
        review.freelancer = booking.freelancer
        review.save()
        return redirect('dashboard')

    return render(request, 'bookings/review.html', {'form': form})


def get_freelancer_rating(freelancer):
    return Review.objects.filter(freelancer=freelancer).aggregate(Avg('rating'))['rating__avg'] or 0