import io
import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
import qrcode
import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

QR_SALT = os.getenv("QR_SALT")
QR_SEPARATOR = os.getenv("QR_SEPARATOR")
# QR_ENCRYPTION_KEY = os.getenv("QR_ENCRYPTION_KEY")
QR_PASSWORD = os.getenv("QR_PASSWORD")
QR_ENCRYPTION_KEY = b"ynJ-_sJjRgJbZbazRVphSwt8UgOb4YzTe5Id0Xw0Gh8="

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_SECRET = os.getenv("CLOUDINARY_SECRET")


def split_decrypted_string(decrypted_text: str):
    clocker_id, card_type = decrypted_text.split(QR_SEPARATOR)

    return clocker_id, card_type


def salt_string(string):
    salt = os.urandom(32)
    salted_bytes = salt + string.encode()

    return salted_bytes


def unsalt_string(salted_bytes):
    return salted_bytes[32:].decode()


def encrypt(prepared_bytes: str):
    key = QR_ENCRYPTION_KEY

    fernet = Fernet(key)
    encrypted_prepared_bytes = fernet.encrypt(prepared_bytes)

    return encrypted_prepared_bytes


def decrypt(encrypted_combined_bytes):
    key = QR_ENCRYPTION_KEY

    fernet = Fernet(key)
    decrypted_combined_bytes = fernet.decrypt(encrypted_combined_bytes)

    return decrypted_combined_bytes


def prepare_qr(email: str, tag_code: str, variant: str):
    combined_string = QR_SEPARATOR.join([email, tag_code])

    salted_bytes = salt_string(combined_string)

    prepared_qr = encrypt(salted_bytes)

    return prepared_qr


def undress_qr_string(encrypted_bytes):
    decrypted_bytes = decrypt(encrypted_bytes)

    unsalted_string = unsalt_string(decrypted_bytes)

    email, tag_code, variant = split_decrypted_string(unsalted_string)

    return {"clocker_id": email, "card_type": tag_code, "variant": variant}


def upload_to_cloudinary(image_data: bytes) -> str:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_SECRET,
    )
    response = cloudinary.uploader.upload(
        file=image_data, folder="clocker/cards/", overwrite=True, resource_type="image"
    )
    return response["secure_url"]


def destroy_from_cloudinary(pic_type: str, url: str) -> str:
    folder = ""
    if pic_type == "tag":
        folder = "databoard/tags/"
    else:
        folder = "databoard/dp/"

    public_id = url.split("/")[-1].split(".")[0]
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_SECRET,
    )

    response = cloudinary.uploader.destroy(folder + public_id)
    return response


def background_color():
    return "#ffffff"


def qr_color():
    return "#000000"


async def qr_logo_url():
    return "https://res.cloudinary.com/dnp0rvouv/image/upload/v1686406100/databoard/logo/databoard_bqxbou.png"


def generate_qr(email: str, tag_code: str, variant: str):
    qr_string = prepare_qr(email, tag_code, variant).decode()

    # logo = Image.open(f'/usr/src/app/img/{qr_logo(card_type=card_type)}')
    logo = Image.open(
        requests.get(
            "https://res.cloudinary.com/dnp0rvouv/image/upload/v1686406100/databoard/logo/databoard_bqxbou.png",
            stream=True,
        ).raw
    )
    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = basewidth / float(logo.size[0])
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        # error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(qr_string)
    QRcode.make()
    back_color = background_color()
    fill_color = qr_color()

    """Set the color of the QR"""
    QRimg = QRcode.make_image(fill_color=fill_color, back_color=back_color).convert(
        "RGB"
    )

    """Set the size of the QR Image"""
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)

    """Add Logo to Generated QR"""
    QRimg.paste(logo, pos)

    """Create a buffer"""
    buffer = io.BytesIO()
    QRimg.save(buffer, format="PNG")
    buffer.seek(0)

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_SECRET,
    )

    response = cloudinary.uploader.upload(
        file=buffer,
        folder="databoard/tags/",
        overwrite=True,
        resource_type="image",
        puplic_id=email,
    )
    return response["secure_url"]
