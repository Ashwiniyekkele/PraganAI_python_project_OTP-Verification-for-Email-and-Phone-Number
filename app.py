import streamlit as st
from twilio.rest import Client


# ============================================================
# TWILIO CONFIGURATION
# ============================================================

# Replace these with your Twilio details
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

# Twilio Verify Service SID
VERIFY_SERVICE_SID = "YOUR_VERIFY_SERVICE_SID"


# Create Twilio client
client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Phone & Email OTP Verification",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "status_message" not in st.session_state:
    st.session_state.status_message = ""

if "status_type" not in st.session_state:
    st.session_state.status_type = "info"

if "phone_otp_sent" not in st.session_state:
    st.session_state.phone_otp_sent = False

if "email_otp_sent" not in st.session_state:
    st.session_state.email_otp_sent = False


# ============================================================
# FUNCTIONS
# ============================================================

def set_status(message, status_type="info"):
    st.session_state.status_message = message
    st.session_state.status_type = status_type


# ------------------------------------------------------------
# SEND PHONE OTP
# ------------------------------------------------------------

def send_phone_otp(phone_number):
    try:
        verification = client.verify.v2.services(
            VERIFY_SERVICE_SID
        ).verifications.create(
            to=phone_number,
            channel="sms"
        )

        if verification.status == "pending":
            st.session_state.phone_otp_sent = True
            set_status(
                "Phone OTP sent successfully.",
                "success"
            )
        else:
            set_status(
                f"Phone OTP status: {verification.status}",
                "info"
            )

    except Exception as e:
        set_status(
            f"Phone OTP error: {str(e)}",
            "error"
        )


# ------------------------------------------------------------
# VERIFY PHONE OTP
# ------------------------------------------------------------

def verify_phone_otp(phone_number, otp):
    try:
        verification_check = client.verify.v2.services(
            VERIFY_SERVICE_SID
        ).verification_checks.create(
            to=phone_number,
            code=otp
        )

        if verification_check.status == "approved":
            set_status(
                "Phone number verified successfully. ✅",
                "success"
            )
        else:
            set_status(
                "Invalid phone OTP.",
                "error"
            )

    except Exception as e:
        set_status(
            f"Phone verification error: {str(e)}",
            "error"
        )


# ------------------------------------------------------------
# SEND EMAIL OTP
# ------------------------------------------------------------

def send_email_otp(email):
    try:
        verification = client.verify.v2.services(
            VERIFY_SERVICE_SID
        ).verifications.create(
            to=email,
            channel="email"
        )

        if verification.status == "pending":
            st.session_state.email_otp_sent = True
            set_status(
                "Email OTP sent successfully.",
                "success"
            )
        else:
            set_status(
                f"Email OTP status: {verification.status}",
                "info"
            )

    except Exception as e:
        set_status(
            f"Email OTP error: {str(e)}",
            "error"
        )


# ------------------------------------------------------------
# VERIFY EMAIL OTP
# ------------------------------------------------------------

def verify_email_otp(email, otp):
    try:
        verification_check = client.verify.v2.services(
            VERIFY_SERVICE_SID
        ).verification_checks.create(
            to=email,
            code=otp
        )

        if verification_check.status == "approved":
            set_status(
                "Email address verified successfully. ✅",
                "success"
            )
        else:
            set_status(
                "Invalid email OTP.",
                "error"
            )

    except Exception as e:
        set_status(
            f"Email verification error: {str(e)}",
            "error"
        )


# ============================================================
# TITLE
# ============================================================

st.title("🔐 Phone & Email OTP Verification")

st.write(
    "Verify your phone number and email address using OTP."
)


# ============================================================
# PHONE VERIFICATION
# ============================================================

st.subheader("📱 Phone Number Verification")

phone_number = st.text_input(
    "Enter Phone Number",
    placeholder="+919876543210"
)

if st.button("Send Phone OTP"):

    if phone_number.strip() == "":
        set_status(
            "Please enter your phone number.",
            "error"
        )

    else:
        send_phone_otp(phone_number)


if st.session_state.phone_otp_sent:

    phone_otp = st.text_input(
        "Enter Phone OTP",
        placeholder="123456",
        key="phone_otp"
    )

    if st.button("Verify Phone OTP"):

        if phone_otp.strip() == "":
            set_status(
                "Please enter the phone OTP.",
                "error"
            )

        else:
            verify_phone_otp(
                phone_number,
                phone_otp
            )


st.divider()


# ============================================================
# EMAIL VERIFICATION
# ============================================================

st.subheader("📧 Email Verification")

email = st.text_input(
    "Enter Email Address",
    placeholder="example@gmail.com"
)

if st.button("Send Email OTP"):

    if email.strip() == "":
        set_status(
            "Please enter your email address.",
            "error"
        )

    else:
        send_email_otp(email)


if st.session_state.email_otp_sent:

    email_otp = st.text_input(
        "Enter Email OTP",
        placeholder="123456",
        key="email_otp"
    )

    if st.button("Verify Email OTP"):

        if email_otp.strip() == "":
            set_status(
                "Please enter the email OTP.",
                "error"
            )

        else:
            verify_email_otp(
                email,
                email_otp
            )


# ============================================================
# STATUS
# ============================================================

st.divider()

st.subheader("📋 Verification Status")

if st.session_state.status_message:

    if st.session_state.status_type == "success":

        st.success(
            st.session_state.status_message
        )

    elif st.session_state.status_type == "error":

        st.error(
            st.session_state.status_message
        )

    else:

        st.info(
            st.session_state.status_message
        )

else:

    st.info(
        "Enter your phone number or email and send an OTP."
      )
