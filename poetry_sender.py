import json
import random
import yagmail
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def load_poetry_database(filename="poetry_database.json"):
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

def save_poetry_database(data, filename="poetry_database.json"):
    """Save the updated poetry database to a JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def select_poem(poetry_data):
    """Randomly select a poem that hasn't been sent yet"""
    # Get all poems that haven't been sent
    available_poems = [poem for poem in poetry_data["poems"] if not poem["sent"]]
    
    # If all poems have been sent, return None or reset all poems
    if not available_poems:
        print("All poems have been sent already!")
        return None
    
    # Randomly select a poem
    selected_poem = random.choice(available_poems)
    return selected_poem

def format_poem(poem):
    """Format the poem nicely for email"""
    lines = poem["lines"]
    title = poem["title"]
    author = poem["author"]
    
    # Format the poem text
    poem_text = "\n".join(lines)
    
    # Create email content
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
    
    return email_content, f"Daily Poem: {title} by {author}"

def send_poem_email(recipient_email, poem):
    """Send the poem via email using yagmail"""
    # Get email credentials from environment variables for security
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")
    
    if not sender_email or not app_password:
        print("Email credentials not found in environment variables!")
        print("Set EMAIL_USER and EMAIL_PASSWORD environment variables.")
        return False
    
    # Format the poem
    email_content, subject = format_poem(poem)
    
    # Send the email
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
    # Configuration - recipient email
    recipient_email = os.getenv("RECIPIENT_EMAIL", "your_email@example.com")
    recipient_email2 = os.getenv("RECIPIENT_EMAIL2", "your_email@example.com")
    # Load the poetry database
    poetry_data = load_poetry_database()
    if not poetry_data:
        print("Failed to load poetry database.")
        return
    
    # Select a random poem
    poem = select_poem(poetry_data)
    if not poem:
        print("No poems available to send.")
        return
    
    # Send the poem via email
    print(f"Sending poem: '{poem['title']}' by {poem['author']}")
    success = send_poem_email(recipient_email, poem)
    
    # Update the database if email was sent successfully
    if success:
        # Mark the poem as sent
        for p in poetry_data["poems"]:
            if p["id"] == poem["id"]:
                p["sent"] = True
                break
        
        # Add to sent list with timestamp
        poetry_data["sent"].append({
            "id": poem["id"],
            "title": poem["title"],
            "author": poem["author"],
            "date_sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Save the updated database
        save_poetry_database(poetry_data)
        print("Poetry database updated successfully.")
        print(f"Email sent successfully to {recipient_email}!")
        send_poem_email(recipient_email2, poem)
        print(f"Email sent successfully to {recipient_email2}!")
    else:
        print("Failed to send email. No changes made to database.")

if __name__ == "__main__":
    main()