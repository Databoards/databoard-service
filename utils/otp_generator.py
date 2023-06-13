import pyotp


def generate_otp():
    # Generate a random base32 string
    base32_string = pyotp.random_base32()

    # Slice the string to get the first 6 characters
    otp = base32_string[:6]
    return otp
