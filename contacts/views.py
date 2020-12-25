from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(user_id=user_id, listing_id=listing_id)
            if has_contacted:
                messages.error(request, 'You Have Already send This Items.')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        send_mail(
            'Property Listing Invoice Request.',
            'There Has Been An Inquiry For ' + listing + '. Sign Into Admin Panel for More Info.',
            'amw@gmail.com',  # Change With Real Mail
            [realtor_email, 'wddh.ahmd@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Successfully Sent Our Realtor Will Contact You Soon. ')
        return redirect('/listings/'+listing_id)
