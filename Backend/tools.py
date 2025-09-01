import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from database import db


@function_tool()
async def get_weather(context: RunContext, city: str) -> str:  # type: ignore
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


@function_tool()
async def search_web(context: RunContext, query: str) -> str:  # type: ignore
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."


@function_tool()
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None,
) -> str:
    """
    Send an email through Gmail.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv(
            "GMAIL_APP_PASSWORD"
        )  # Use App Password, not regular password

        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables")
            return "Email sending failed: Gmail credentials not configured."

        # Create message
        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = to_email
        msg["Subject"] = subject

        # Add CC if provided
        recipients = [to_email]
        if cc_email:
            msg["Cc"] = cc_email
            recipients.append(cc_email)

        # Attach message body
        msg.attach(MIMEText(message, "plain"))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(gmail_user, gmail_password)

        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()

        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"

    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"


@function_tool()
async def update_user_details(
    context: RunContext,  # type: ignore
    user_id: int,
    phone_number: Optional[str] = None,
    email_password: Optional[str] = None,
    backup_email: Optional[str] = None,
    address: Optional[str] = None,
) -> str:
    """
    Update user's contact details that can be used by Friday's tools.

    Args:
        user_id: User's ID
        phone_number: User's phone number
        email_password: User's email app password for sending emails
        backup_email: User's backup email address
        address: User's physical address
    """
    try:
        success = db.set_user_details(
            user_id=user_id,
            phone_number=phone_number,
            email_password=email_password,
            backup_email=backup_email,
            address=address,
        )

        if success:
            logging.info(f"Updated details for user {user_id}")
            return "Your contact details have been updated successfully."
        else:
            return "I had trouble updating your details. Please try again."

    except Exception as e:
        logging.error(f"Error updating user details: {e}")
        return "I encountered an error while updating your details."


@function_tool()
async def get_my_details(context: RunContext, user_id: int) -> str:  # type: ignore
    """
    Get the user's stored contact details.

    Args:
        user_id: User's ID
    """
    try:
        user = db.get_user_by_id(user_id)
        details = db.get_user_details(user_id)

        if not user:
            return "I couldn't find your user information."

        info = [f"Name: {user['name']}", f"Email: {user['email']}"]

        if details:
            if details["phone_number"]:
                info.append(f"Phone: {details['phone_number']}")
            if details["backup_email"]:
                info.append(f"Backup Email: {details['backup_email']}")
            if details["address"]:
                info.append(f"Address: {details['address']}")

        return f"Here are your details: {', '.join(info)}"

    except Exception as e:
        logging.error(f"Error getting user details: {e}")
        return "I encountered an error while retrieving your details."
