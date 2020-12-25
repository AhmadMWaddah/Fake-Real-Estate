from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        # Get Form Values.
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Password Match Validation.
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User Name Is Already Registered.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'E-Mail Is Already Registered.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Successfully Registered, Please Log In.')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords Does Not Match.')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully Logged In.')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid Credentials.')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successfully Logged out.')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
