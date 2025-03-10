import json
import random
import yagmail
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load local .env file if present
load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Send a daily poem via email."
    )
    parser.add_argument(
        "--email-user",
        default=os.getenv("EMAIL_USER"),
        help="Sender email address (defaults to EMAIL_USER env var)"
    )
    parser.add_argument(
        "--email-password",
        default=os.getenv("EMAIL_PASSWORD"),
        help="Sender email app password (defaults to EMAIL_PASSWORD env var)"
    )
    parser.add_argument(
        "--recipient-email",
        default=os.getenv("RECIPIENT_EMAIL", "your_email@example.com"),
        help="Primary recipient email address (defaults to RECIPIENT_EMAIL env var)"
    )
    parser.add_argument(
        "--recipient-email2",
        default=os.getenv("RECIPIENT_EMAIL2", "your_email@example.com"),
        help="Secondary recipient email address (defaults to RECIPIENT_EMAIL2 env var)"
    )
    return parser.parse_args()

def load_poetry_database(filename="short_poetries.json"):
    """Load the poetry database from a JSON file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return None
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON!")
        return None

def save_poetry_database(data, filename="short_poetries.json"):
    """Save the updated poetry database to a JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def select_poem(poetry_data):
    """Randomly select a poem that hasn't been sent yet"""
    available_poems = [poem for poem in poetry_data["poems"] if not poem.get("sent")]
    
    if not available_poems:
        print("All poems have been sent already!")
        return None
    
    selected_poem = random.choice(available_poems)
    return selected_poem

def format_poem(poem):
    """Format the poem nicely for email"""
    lines = poem["lines"]
    title = poem["title"]
    author = poem["author"]
    
    poem_text = "\n".join(lines)
    
    email_content = f"""
    <html>
      <body>
        <h2>{title}</h2>
        <h3>by {author}</h3>
        <pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">
{poem_text}
        </pre>
        <p><i>Poem of the day - {datetime.now().strftime('%Y-%m-%d')}</i></p>
      </body>
    </html>
    """
    subject = f"Daily Poem: {title} by {author}"
    return email_content, subject

def send_poem_email(sender_email, app_password, recipient_email, poem):
    """Send the poem via email using yagmail"""
    if not sender_email or not app_password:
        print("Email credentials not found!")
        print("Set EMAIL_USER and EMAIL_PASSWORD environment variables or pass via command-line arguments.")
        return False
    
    email_content, subject = format_poem(poem)
    
    try:
        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=email_content
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    args = parse_args()
    sender_email = args.email_user
    app_password = args.email_password
    recipient_email = args.recipient_email
    recipient_email2 = args.recipient_email2

    poetry_data = load_poetry_database()
    if not poetry_data:
        print("Failed to load poetry database.")
        return
    
    poem = select_poem(poetry_data)
    if not poem:
        print("No poems available to send.")
        return
    
    print(f"Sending poem: '{poem['title']}' by {poem['author']}")
    success = send_poem_email(sender_email, app_password, recipient_email, poem)
    
    if success:
        # Mark the poem as sent
        for p in poetry_data["poems"]:
            if p["id"] == poem["id"]:
                p["sent"] = True
                break
        
        poetry_data.setdefault("sent", []).append({
            "id": poem["id"],
            "title": poem["title"],
            "author": poem["author"],
            "date_sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_poetry_database(poetry_data)
        print("Poetry database updated successfully.")
        print(f"Email sent successfully to {recipient_email}!")
        # Send to second recipient
        if send_poem_email(sender_email, app_password, recipient_email2, poem):
            print(f"Email sent successfully to {recipient_email2}!")
        else:
            print(f"Failed to send email to {recipient_email2}.")
    else:
        print("Failed to send email. No changes made to database.")

if __name__ == "__main__":
    main()
