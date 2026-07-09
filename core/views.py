from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, BloodRequest, Inventory
from django.contrib import messages

def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        phone = request.POST['phone']
        location = request.POST['location']
        blood_group = request.POST.get('blood_group', '')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = role
        user.phone = phone
        user.location = location
        user.blood_group = blood_group
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard(request):
    if request.user.role == 'hospital':
        return redirect('hospital_dashboard')
    elif request.user.role == 'bloodbank':
        return redirect('bloodbank_dashboard')
    else:
        return redirect('donor_dashboard')

@login_required
def hospital_dashboard(request):
    if request.method == 'POST':
        blood_type = request.POST['blood_type']
        units_needed = request.POST['units_needed']
        urgency = request.POST['urgency']
        BloodRequest.objects.create(
            hospital=request.user,
            blood_type=blood_type,
            units_needed=units_needed,
            urgency=urgency
        )
        messages.success(request, 'Blood request posted successfully!')
    requests = BloodRequest.objects.filter(hospital=request.user).order_by('-created_at')
    return render(request, 'hospital_dashboard.html', {'requests': requests})

@login_required
@login_required
def bloodbank_dashboard(request):
    if request.method == 'POST':
        blood_type = request.POST['blood_type']
        units_available = request.POST['units_available']
        expiry_date = request.POST['expiry_date']
        Inventory.objects.create(
            blood_bank=request.user,
            blood_type=blood_type,
            units_available=units_available,
            expiry_date=expiry_date
        )
        messages.success(request, 'Inventory updated successfully!')
    incoming = BloodRequest.objects.filter(status='pending').order_by('-created_at')
    inventory = Inventory.objects.filter(blood_bank=request.user)
    return render(request, 'bloodbank_dashboard.html', {'incoming': incoming, 'inventory': inventory})

@login_required
def fulfill_request(request, request_id):
    blood_request = BloodRequest.objects.get(id=request_id)
    blood_request.status = 'fulfilled'
    blood_request.save()
    return redirect('bloodbank_dashboard')

@login_required
def donor_dashboard(request):
    active_requests = BloodRequest.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'donor_dashboard.html', {'active_requests': active_requests})

def request_board(request):
    active_requests = BloodRequest.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'request_board.html', {'active_requests': active_requests})
@login_required
def donor_respond(request, request_id):
    blood_request = BloodRequest.objects.get(id=request_id)
    blood_request.status = 'matched'
    blood_request.save()
    messages.success(request, 'Thank you! The hospital has been notified of your availability.')
    return redirect('donor_dashboard')