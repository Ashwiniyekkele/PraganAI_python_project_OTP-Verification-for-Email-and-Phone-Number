
import os
import time
import secrets
import smtplib
import streamlit as st

from email.message import EmailMessage
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="OTP Verification System",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 PragyanAI OTP Verification System")
st.write("Verify your email address and phone number securely using OTPs.")

OTP_EXPIRY = 300  # 5 minutes


# ---------------- LOAD SECRETS ----------------

def get_secret(key):
    """Read a secret from Streamlit secrets or environment variables."""
    try:
        value = st.secrets.get(key)
        if value:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv(key, "").strip()


EMAIL_ADDRESS = get_secret("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = get_secret("EMAIL_APP_PASSWORD")

TWILIO_ACCOUNT_SID = get_secret("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_secret("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = get_secret(
    "TWILIO_VERIFY_SERVICE_SID"
)


# ---------------- INITIALIZE SESSION STATE ----------------

defaults = {
    "email_otp": None,
    "email_otp_time": None,
    "email_verified": False,
    "phone_verification_sent": False,
    "phone_verified": False,
    "phone_number": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- EMAIL OTP FUNCTIONS ----------------

def send_email_otp(email):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        st.error(
            "Email credentials are missing. "
            "Configure EMAIL_ADDRESS and EMAIL_APP_PASSWORD."
        )
        return

    otp = f"{secrets.randbelow(900000) + 100000}"

    message = EmailMessage()
    message["Subject"] = "Your PragyanAI Verification OTP"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email
    message.set_content(
        f"Your OTP is: {otp}\n\n"
        "This OTP expires in 5 minutes. "
        "Do not share it with anyone."
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(message)

        st.session_state.email_otp = otp
        st.session_state.email_otp_time = time.time()
        st.session_state.email_verified = False

        st.success("Email OTP sent successfully!")

    except smtplib.SMTPAuthenticationError:
        st.error(
            "Gmail authentication failed. Check your Gmail address "
            "and 16-character Google App Password."
        )
    except Exception as e:
        st.error(f"Email sending failed: {e}")


def verify_email_otp(user_otp):
    stored_otp = st.session_state.email_otp
    sent_time = st.session_state.email_otp_time

    if not stored_otp or sent_time is None:
        st.error("Please request an email OTP first.")
        return

    if time.time() - sent_time > OTP_EXPIRY:
        st.session_state.email_otp = None
        st.session_state.email_otp_time = None
        st.error("OTP expired. Please request a new OTP.")
        return

    if secrets.compare_digest(user_otp.strip(), stored_otp):
        st.session_state.email_verified = True
        st.session_state.email_otp = None
        st.success("Email verified successfully!")
    else:
        st.error("Incorrect OTP. Please try again.")


# ---------------- TWILIO PHONE OTP FUNCTIONS ----------------

def send_phone_otp(phone_number):
    if not all([
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN,
        TWILIO_VERIFY_SERVICE_SID,
    ]):
        st.error(
            "Twilio credentials are missing. Check your Streamlit secrets."
        )
        return

    if not TWILIO_ACCOUNT_SID.startswith("AC"):
        st.error("Your Twilio Account SID should start with AC.")
        return

    if not TWILIO_VERIFY_SERVICE_SID.startswith("VA"):
        st.error("Your Verify Service SID should start with VA.")
        return

    phone_number = phone_number.strip()

    if not phone_number.startswith("+") or not phone_number[1:].isdigit():
        st.error(
            "Enter a valid international phone number, "
            "including country code, e.g. +919876543210."
        )
        return

    try:
        client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        verification = client.verify.v2.services(
            TWILIO_VERIFY_SERVICE_SID
        ).verifications.create(
            to=phone_number,
            channel="sms"
        )

        st.session_state.phone_number = phone_number
        st.session_state.phone_verification_sent = True
        st.session_state.phone_verified = False

        st.success(
            f"Twilio accepted the verification request. "
            f"Status: {verification.status}"
        )

    except TwilioRestException as e:
        # Helpful diagnostic; never display account credentials.
        st.error(f"Twilio error code: {e.code}")
        st.error(f"Twilio message: {e.msg}")

        if e.code == 20003:
            st.warning(
                "Authentication failed. Check your Account SID and Auth Token."
            )
        elif e.code == 60200:
            st.warning(
                "The request contains an invalid parameter. "
                "Check the phone number and Verify Service SID."
            )
        elif e.code == 60203:
            st.warning(
                "The maximum number of verification attempts may have "
                "been reached. Wait before trying again."
            )
        elif e.code == 60205:
            st.warning(
                "The destination may not be reachable by this Verify service."
            )
        else:
            st.info(
                "Check the Twilio Verify error-code documentation for this code."
            )

    except Exception as e:
        st.error(
            f"Application error: {type(e).__name__}: {e}"
        )


def check_phone_otp(user_otp):
    if not st.session_state.phone_verification_sent:
        st.error("Please request an SMS OTP first.")
        return

    if not TWILIO_VERIFY_SERVICE_SID:
        st.error("Twilio Verify Service SID is missing.")
        return

    try:
        client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        result = client.verify.v2.services(
            TWILIO_VERIFY_SERVICE_SID
        ).verification_checks.create(
            to=st.session_state.phone_number,
            code=user_otp.strip()
        )

        if result.status == "approved":
            st.session_state.phone_verified = True
            st.session_state.phone_verification_sent = False
            st.success("Phone number verified successfully!")
        else:
            st.error("Incorrect or expired OTP. Please try again.")

    except TwilioRestException as e:
        st.error(f"Twilio verification error code: {e.code}")
        st.error(f"Twilio message: {e.msg}")

    except Exception as e:
        st.error(
            f"Application error: {type(e).__name__}: {e}"
        )


# ---------------- EMAIL VERIFICATION UI ----------------

st.divider()
st.subheader("📧 Email Verification")

email = st.text_input(
    "Enter your email address",
    key="email_input",
    placeholder="example@gmail.com"
)

if st.button("Send Email OTP", use_container_width=True):
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        st.error("Please enter a valid email address.")
    else:
        send_email_otp(email.strip())

if st.session_state.email_otp:
    email_code = st.text_input(
        "Enter the email OTP",
        max_chars=6,
        key="email_code"
    )

    if st.button("Verify Email OTP", use_container_width=True):
        if len(email_code.strip()) != 6 or not email_code.strip().isdigit():
            st.error("Enter the six-digit OTP.")
        else:
            verify_email_otp(email_code)


if st.session_state.email_verified:
    st.success("✅ Email verification completed.")


# ---------------- PHONE VERIFICATION UI ----------------

st.divider()
st.subheader("📱 Phone Verification")

phone = st.text_input(
    "Enter your phone number with country code",
    placeholder="+919876543210"
)

if st.button("Send SMS OTP", use_container_width=True):
    send_phone_otp(phone)

if st.session_state.phone_verification_sent:
    phone_code = st.text_input(
        "Enter the SMS OTP",
        max_chars=10,
        key="phone_code"
    )

    if st.button("Verify Phone OTP", use_container_width=True):
        if not phone_code.strip().isdigit():
            st.error("Enter the numeric OTP received by SMS.")
        else:
            check_phone_otp(phone_code)


if st.session_state.phone_verified:
    st.success("✅ Phone verification completed.")


# ---------------- FINAL STATUS ----------------

st.divider()
st.subheader("📋 Verification Status")

st.write(
    f"Email: {'Verified ✅' if st.session_state.email_verified else 'Not verified'}"
)

st.write(
    f"Phone: {'Verified ✅' if st.session_state.phone_verified else 'Not verified'}"
)

if st.session_state.email_verified and st.session_state.phone_verified:
    st.balloons()
    st.success("🎉 Both email and phone verification are complete!")
