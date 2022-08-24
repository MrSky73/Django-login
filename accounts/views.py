from email import message
from django.shortcuts import render
from rest_framework.response import Response
from .helpers import send_otp_to_phone
from .models import User
from rest_framework.decorators import api_view
from django.shortcuts import redirect
import random


def home_view(request):
    # logic of view will be implemented here
    return render(request, "home.html")


def verify_view(request):
    return render(request, "verify.html")


def end_view(request):
    return render(request, 'end.html', {'message': 'hello there'})


@api_view(['POST'])
def send_otp(requests):
    data = requests.data
    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': 'key phone_number is required'
        })
    # if data.get('password') is None:
    #     return Response({
    #         'status': 400,
    #         'message': 'key password is required'
    #     })
    otp = send_otp_to_phone(data.get('phone_number'))
    phone_number = data.get('phone_number')
    user = User.objects.create(
        username=random.randint(10000000, 99999999), phone_number=phone_number, otp=otp)
    # user.set_password = data.get('set_password')
    user.save()
    return redirect('/verify/')
    # return Response({
    #     'status': 200,
    #     'message': 'otp sent'
    # })


@api_view(['POST'])
def verify_otp(requests):
    data = requests.data

    # if data.get('phone_number') is None:
    #     return Response({
    #         'status': 400,
    #         'message': 'key phone_number is required'
    #     })

    if data.get('otp') is None:
        message = 'key otp is required'

    try:
        user_obj = User.objects.last()

    except Exception as e:
        message = 'Invalid phone'

    # if user_obj.phone_number != data.get('phone_number'):
    #     return Response({
    #         'status': 400,
    #         'message': 'Invalid phone'
    #     })

    if user_obj.otp == data.get('otp'):
        message = 'otp matched'

    else:
        message = 'otp Invalid'
    return render(requests, 'end.html', {'message': message})
