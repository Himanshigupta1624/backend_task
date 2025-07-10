# Email Campaign Manager

A Django application for managing email campaigns and subscribers with asynchronous email sending capabilities using Celery.

## Features

- 📧 Create and manage email campaigns
- 👥 Manage subscribers with automatic tracking
- 🔄 Asynchronous email sending with Celery
- 📨 Email template system
- 📊 Admin interface for campaign and subscriber management
- 🔓 Unsubscribe functionality
- 📱 Responsive subscription form

## Technology Stack

- Django 4.2
- Celery 5.3.4
- Redis (message broker)
- SQLite (database)
- Django REST Framework
- Mailgun SMTP (email delivery)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Redis server
- Mailgun account (or another SMTP provider)

### Installation

1. Clone the repository:
git clone https://github.com/Himanshigupta1624/backend_task.git
- cd email-manager
2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
- Windows:
  ```
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Create a `.env` file in the project root:
```EMAIL_HOST=smtp.mailgun.org EMAIL_PORT=587
 EMAIL_HOST_USER=your_mailgun_user
 EMAIL_HOST_PASSWORD=your_mailgun_password
DEFAULT_FROM_EMAIL=your_from_email
```

6. Run migrations:
```
python manage.py migrate
```

### Running the Application

1. Start the Django development server:
```
python manage.py runserver
```

2. Start the Celery worker:
- Windows:
  ```
  celery -A email_manager worker --loglevel=info --pool=solo
  ```
- macOS/Linux:
  ```
  celery -A email_manager worker --loglevel=info
  ```

## Usage

### Creating Campaigns

1. Log in to the admin interface at `http://localhost:8000/admin/`
2. Navigate to "Campaigns" and click "Add Campaign"
3. Fill in the campaign details:
- Subject: Email subject line
- Preview Text: Short preview shown in email clients
- Article URL: Link to the main content
- HTML Content: HTML-formatted email content
- Plain Text Content: Plain text version of the email
4. Click "Save"

### Managing Subscribers

1. From the admin interface, navigate to "Subscribers"
2. Click "Add Subscriber" to add subscribers manually, or
3. Direct users to the subscription form at `http://localhost:8000/emails/`

### Sending Campaigns

You can send campaigns in several ways:

1. **Via Management Command**:
- Send synchronously :- 
```python manage.py send_campaign <campaign_id>```

- Send asynchronously with Celery :-
```python manage.py send_campaign <campaign_id> --async```
2. **Via API Endpoint**:
- Send campaign immediately:-
```POST /emails/send-campaign/<campaign_id>/```

- Schedule daily campaign:-
```POST /emails/schedule-campaign/<campaign_id>/```

### Unsubscribing

Users can unsubscribe via the unsubscribe link: `http://localhost:8000/emails/unsubscribe/<email>/`





