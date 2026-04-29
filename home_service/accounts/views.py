from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import RegisterForm,FreelancerProfileForm,ClientProfileForm
from bookings.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.models import Notification,FreelancerProfile,ClientProfile
from django.db.models import Avg
from bookings.models import Booking, Review
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        # 🔔 Notify admin(s)
        admins = User.objects.filter(is_superuser=True)

        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"🆕 New user registered: {user.username}"
            )

        return redirect('login')

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Redirect based on user type
            if user.user_type == 'client':
                return redirect('/services/')   # 👈 show services

            elif user.user_type == 'freelancer':
                return redirect('dashboard')      # 👈 show bookings

            else:
                return redirect('dashboard')  # fallback

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('home') 


@require_POST
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)

    # ensure only the assigned freelancer can update
    if request.user != booking.freelancer:
        return redirect('dashboard')

    if action == 'accept':
        booking.status = 'accepted'
        Notification.objects.create(
            user = booking.client,
            message="Your booking was accepted"
        )
    elif action == 'reject':
        booking.status = 'cancelled'
        Notification.objects.create(
            user=booking.client,
            message="You was rejected"
        )

    booking.save()
    return redirect('dashboard')    
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notes': notes})
@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')

    if user.user_type == 'client':
        bookings = Booking.objects.filter(client=user).order_by('-created_at')

        for b in bookings:
            b.has_review = Review.objects.filter(booking=b).exists()

        # optional: attach review object if exists
            b.review = Review.objects.filter(booking=b).first()

        return render(request, 'client_dashboard.html', {
        'bookings': bookings
            })

    # FREELANCER DASHBOARD
    elif user.user_type == 'freelancer':
        bookings = Booking.objects.filter(freelancer=user).order_by('-created_at')

        reviews = Review.objects.filter(freelancer=user).order_by('-created_at')

        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        return render(request, 'freelancer_dashboard.html', {
            'bookings': bookings,
            'reviews': reviews,
            'avg_rating': avg_rating
                })

    # fallback (optional safety)
    return redirect('home')
def update_booking(request, booking_id, action):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)

        if request.user != booking.freelancer:
            return redirect('dashboard')

        if action == 'accept':
            booking.status = 'accepted'

            Notification.objects.create(
                user=booking.client,
                message=f"✅ Your booking for {booking.service.name} was ACCEPTED"
            )

        elif action == 'reject':
            booking.status = 'cancelled'

            Notification.objects.create(
                user=booking.client,
                message=f"❌ Your booking for {booking.service.name} was REJECTED"
            )

        elif action == 'complete':
            booking.status = 'completed'

            Notification.objects.create(
                user=booking.client,
                message=f"🎉 Your booking for {booking.service.name} is COMPLETED. Please leave a review!"
            )

        booking.save()

    return redirect('dashboard')

@login_required
def edit_freelancer_profile(request):
    profile = request.user.freelancerprofile

    form = FreelancerProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'edit_freelancerprofile.html', {
        'form': form
    })
@login_required
def edit_client_profile(request):
    profile, created = ClientProfile.objects.get_or_create(user=request.user)

    form = ClientProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'edit_clientprofile.html', {
        'form': form
    })


def admin_dashboard(request):
    total_services = Service.objects.count()
    total_users = User.objects.count()
    total_freelancers = FreelancerProfile.objects.count()
    total_clients = ClientProfile.objects.count()

    services = Service.objects.all()

    return render(request, 'admin_dashboard.html', {
        'total_services': total_services,
        'total_users': total_users,
        'total_freelancers': total_freelancers,
        'total_clients': total_clients,
        'services': services
    })


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_users.html', {'users': users})
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_users')
@user_passes_test(is_admin)
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'admin_bookings.html', {'bookings': bookings})


def view_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    review = get_object_or_404(Review, booking=booking)

    return render(request, 'view_review.html', {
        'review': review
    })