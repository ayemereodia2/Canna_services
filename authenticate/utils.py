from .models import CustomUser, OneTimePassword
import random


def generateOtp():
    otp = ""
    for i in range(4):
        otp += str(random.randint(1, 9))
    return otp
