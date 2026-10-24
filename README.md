# 🔐 PragyanAI OTP Verification System

A Python-based web application that verifies users' email addresses and phone numbers using One-Time Passwords (OTPs). The application uses **Streamlit** for the user interface, **Gmail SMTP** for email OTP delivery, and **Twilio Verify** for SMS OTP verification.

## 🌐 Live Streamlit Application

The PragyanAI OTP Verification System is built using Streamlit, providing an interactive web interface for email and phone number verification.

🚀 **Try the Live Application:** [Open Streamlit App](https://pragyanaipythonotpverificationsystem-osbhjbz3lcnxungxiedyqq.streamlit.app/)

### Features
- 📧 Email OTP verification using Gmail SMTP.
- 📱 SMS OTP verification using Twilio Verify.
- ⏱️ Five-minute expiry for email OTPs.
- ✅ Real-time verification status.

**Note:** Replace `YOUR_STREAMLIT_APP_URL` with your actual deployed Streamlit URL, for example `https://your-app-name.streamlit.app`.

## 🚀 Features

- 📧 **Email OTP Verification** – Sends a six-digit OTP to the user's email address.
- 📱 **Phone OTP Verification** – Sends SMS verification codes using Twilio Verify.
- 🔒 **Secure OTP Generation** – Generates cryptographically secure six-digit email OTPs.
- ⏱️ **OTP Expiration** – Email OTPs expire after five minutes.
- ✅ **Verification Status** – Displays success and error messages for email and phone verification.
- 🔑 **Secrets Management** – Stores credentials using Streamlit secrets or environment variables.
- 🌐 **Web Application** – Provides a simple, interactive interface built with Streamlit.
- ☁️ **Cloud Deployment** – Supports deployment on Streamlit Community Cloud.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and OTP generation |
| Streamlit | Web interface |
| Gmail SMTP | Email OTP delivery |
| Twilio Verify API | SMS OTP delivery and verification |
| `secrets` | Secure OTP generation |
| `smtplib` | Sending email messages |
| Git and GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Web application deployment |

## 📁 Project Structure

```text
PragyanAI-OTP-Verification-System/
│
├── app.py
├── requirements.txt
├── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PragyanAI-OTP-Verification-System.git
```

Navigate to the project directory:

```bash
cd PragyanAI-OTP-Verification-System
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Configuration and Secret Keys

The application requires Gmail and Twilio credentials to send and verify OTPs.

Create a file named `.streamlit/secrets.toml` and add the following configuration:

```toml
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_APP_PASSWORD = "your-gmail-app-password"

TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_VERIFY_SERVICE_SID = "your-verify-service-sid"
```

Replace the placeholders with your actual credentials.

### Gmail Configuration

1. Open your [Google Account Security settings](https://myaccount.google.com/security).
2. Enable 2-Step Verification.
3. Generate a Google App Password if your account supports it.
4. Set `EMAIL_ADDRESS` and `EMAIL_APP_PASSWORD`.

### Twilio Configuration

1. Sign in to the [Twilio Console](https://console.twilio.com/).
2. Copy your Account SID and Auth Token.
3. Create a service in [Twilio Verify](https://console.twilio.com/us1/develop/verify/services).
4. Copy the Verify Service SID.
5. Add all three values to your secrets configuration.

**Security warning:** Never publish passwords, authentication tokens, or API credentials in your source code or public GitHub repository.

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📱 How to Use

### Email Verification

1. Enter your email address.
2. Click **Send Email OTP**.
3. Check your inbox for the verification code.
4. Enter the six-digit OTP.
5. Click **Verify Email**.
6. View the verification result.

### Phone Verification

1. Enter your phone number in international format, such as `+919876543210`.
2. Click **Send SMS OTP**.
3. Enter the code received on your phone.
4. Click **Verify Phone**.
5. View the verification result.

Phone verification is handled by Twilio Verify, which manages the SMS code and its validity.

## ☁️ Deployment on Streamlit Community Cloud

1. Push the project files to GitHub.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with your GitHub account.
4. Create a new app and select your repository.
5. Set the main file path to `app.py`.
6. Open the app settings and locate **Secrets**.
7. Add the required credentials in TOML format.
8. Deploy the application.

Once deployment succeeds, Streamlit will provide a public URL for your application.

## 📦 Requirements

The project dependencies are listed in `requirements.txt`:

```text
streamlit
twilio
```

## 🔒 Security Considerations

- Never commit `.streamlit/secrets.toml` to GitHub.
- Use Google App Passwords instead of your regular Gmail password.
- Protect your Twilio Auth Token.
- Email OTPs expire after five minutes.
- Twilio Verify manages phone verification codes.
- Add rate limiting, verification attempt limits, and persistent server-side verification records before using the application in production.
- Avoid exposing sensitive credentials or detailed internal errors in user-facing messages.

## 🐛 Troubleshooting

**Email OTP is not sent**
- Verify the Gmail address and App Password.
- Ensure 2-Step Verification and App Password access are configured correctly.
- Check SMTP connectivity and account restrictions.

**SMS OTP is not sent**
- Verify your Twilio Account SID, Auth Token, and Verify Service SID.
- Check your Twilio account status, billing, and destination restrictions.
- Ensure the phone number includes the country code.
- Check the actual Twilio error code for more information.

**Application fails to start**
- Install dependencies using `pip install -r requirements.txt`.
- Confirm that the main file is named `app.py`.
- Check the Streamlit Cloud deployment logs for configuration errors.

## 🎯 Project Objective

The objective of this project is to demonstrate OTP-based email and phone verification using Python and third-party communication services. It provides practical experience with web application development, API integration, credential management, and cloud deployment.

## 👨‍💻 Author

**Ashwini yekkele**
