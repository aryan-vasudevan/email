import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import time
from openai import OpenAI

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Initialize OpenAI client
client = OpenAI(
    api_key="api key"
)
model = "gpt-3.5-turbo"

def authenticate_gmail():
    """Authenticate and return Gmail service object"""
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def generate_email_with_gpt(person_info, goal, sender_info):
    """Use ChatGPT to generate personalized email subject and body"""
    
    prompt = f"""
    Create a professional, personalized email for the following scenario:

    SENDER INFORMATION:
    - Name: {sender_info.get('name', '[Your Name]')}
    - Company: {sender_info.get('company', '[Your Company]')}
    - Role: {sender_info.get('role', '[Your Role]')}
    - Purpose: {goal}

    RECIPIENT INFORMATION:
    - Name: {person_info.get('name', 'there')}
    - Email: {person_info.get('email')}
    - Company: {person_info.get('company', 'their company')}
    - Role: {person_info.get('role', 'professional')}
    - Location: {person_info.get('location', 'N/A')}
    - Interests: {', '.join(person_info.get('interests', []))}

    REQUIREMENTS:
    1. Create a compelling subject line (max 60 characters)
    2. Write a personalized email body (200-300 words)
    3. Make it professional but warm
    4. Include specific references to their company, role, and interests when relevant
    5. Include a clear call-to-action
    6. End with the sender's name

    GOALS CONTEXT:
    - partnership: seeking business collaboration
    - hiring: recruiting for a position
    - sales: selling a product/service
    - networking: building professional relationships
    - collaboration: project collaboration
    - general: general outreach

    Please format your response as:
    SUBJECT: [subject line here]
    
    BODY:
    [email body here]
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional email writer who creates compelling, personalized business emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse the response
        if "SUBJECT:" in content and "BODY:" in content:
            parts = content.split("BODY:")
            subject = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip()
            return subject, body
        else:
            # Fallback if parsing fails
            return f"Professional Outreach - {person_info.get('company', 'Opportunity')}", content
            
    except Exception as e:
        print(f"Error generating email with GPT: {e}")
        # Fallback to simple template
        return generate_fallback_email(person_info, goal)

def generate_fallback_email(person_info, goal):
    """Fallback email generation if GPT fails"""
    name = person_info.get('name', 'there')
    company = person_info.get('company', 'your company')
    role = person_info.get('role', 'professional')
    
    subject = f"Reaching out to {company}"
    body = f"""Hi {name},

I hope this email finds you well. I wanted to reach out regarding your work as {role} at {company}.

I believe there may be opportunities for us to connect and explore potential collaboration.

Would you be open to a brief conversation?

Best regards,
[Your Name]"""
    
    return subject, body

def create_message(sender, to, subject, message_text):
    """Create email message"""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message, recipient_name):
    """Send email message"""
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'✅ Email sent successfully to {recipient_name}! Message ID: {sent_message["id"]}')
        return sent_message
    except Exception as error:
        print(f'❌ Error sending email to {recipient_name}: {error}')
        return None

def send_ai_personalized_emails():
    """Main function to send AI-generated personalized emails"""
    
    # YOUR INFORMATION (Fill this out)
    sender_info = {
        'name': 'Your Name Here',
        'company': 'Your Company',
        'role': 'Your Role'
    }
    
    # Your goal for reaching out
    CONTACT_GOAL = "partnership"  # Options: partnership, hiring, sales, networking, collaboration, general
    
    # List of recipients with their information
    recipients = [
        {
            'email': 'nathanyan2008p@gmail.com',
            'name': 'Nathan',
            'company': 'Tech Innovations Inc',
            'role': 'Software Engineer',
            'location': 'San Francisco',
            'interests': ['AI', 'machine learning', 'startups']
        },
        {
            'email': 'nathanyan2008p@gmail.com',
            'name': 'John Doe',
            'company': 'Data Solutions LLC',
            'role': 'Data Scientist',
            'location': 'New York',
            'interests': ['data analytics', 'Python', 'cloud computing']
        },
        {
            'email': 'nathanyan2008p@gmail.com',
            'name': 'Jane Smith',
            'company': 'Marketing Pro',
            'role': 'Marketing Director',
            'location': 'Chicago',
            'interests': ['digital marketing', 'growth hacking', 'analytics']
        }
    ]
    
    # Authenticate Gmail
    service = authenticate_gmail()
    
    print(f"🚀 Starting AI-powered email campaign...")
    print(f"📧 Recipients: {len(recipients)}")
    print(f"🎯 Goal: {CONTACT_GOAL}")
    print(f"🤖 Using GPT for personalization")
    print("-" * 60)
    
    successful_sends = 0
    
    for i, person in enumerate(recipients, 1):
        try:
            print(f"\n[{i}/{len(recipients)}] 🤖 Generating email for {person['name']}...")
            
            # Generate email using GPT
            subject, email_body = generate_email_with_gpt(person, CONTACT_GOAL, sender_info)
            
            print(f"📋 Subject: {subject}")
            print(f"📝 Preview: {email_body[:100]}...")
            
            # Create and send message
            message = create_message("me", person['email'], subject, email_body)
            result = send_message(service, "me", message, person['name'])
            
            if result:
                successful_sends += 1
            
            # Add delay between emails
            if i < len(recipients):
                print("⏳ Waiting 3 seconds before next email...")
                time.sleep(3)
                
        except Exception as e:
            print(f"❌ Error processing {person['name']}: {e}")
    
    print(f"\n" + "="*60)
    print(f"🎉 AI Email Campaign Completed!")
    print(f"✅ Successfully sent: {successful_sends}/{len(recipients)} emails")
    print(f"🎯 Goal: {CONTACT_GOAL}")
    print(f"🤖 Powered by ChatGPT")

if __name__ == "__main__":
    # OpenAI client is already initialized with your API key
    send_ai_personalized_emails()