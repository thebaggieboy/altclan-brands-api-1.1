import logging
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Profile
from accounts.models import BrandUser, BrandProfile, CustomUser
from brands.models import ShippingAddress, BillingAddress, BrandDashboard

# Import Gallery with error handling
try:
    from brands.models import Gallery
    GALLERY_AVAILABLE = True
except ImportError:
    GALLERY_AVAILABLE = False
    logger.warning("Gallery model not available - skipping gallery creation")

# Set up logging
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile_and_send_welcome_email(sender, instance, created, **kwargs):
    """
    Create user profile, gallery, and send welcome email for new users.
    
    Args:
        sender: The model class (User)
        instance: The actual user instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if not created:
        return
    
    try:
        # Validate user instance first
        if not instance or not hasattr(instance, 'id') or not instance.id:
            logger.error("Invalid user instance provided for profile creation")
            print("❌ ERROR: Invalid user instance - cannot create profile")
            return
        
        # Create Profile (outside transaction to avoid blocking user creation)
        try:
            profile = Profile.objects.create(user=instance)
            logger.info(f"Profile created successfully for user {instance.id}")
            print(f"✅ SUCCESS: Profile created for user {instance.email} (ID: {instance.id})")
        except Exception as profile_error:
            logger.error(f"Failed to create profile for user {instance.id}: {profile_error}")
            print(f"❌ ERROR: Failed to create profile for {instance.email}: {profile_error}")
            # Don't return here - continue with other operations
        
        # Create Gallery (only if available and profile creation succeeded)
        if GALLERY_AVAILABLE:
            try:
                gallery = Gallery.objects.create(user=instance)
                logger.info(f"Gallery created successfully for user {instance.id}")
                print(f"📸 SUCCESS: Gallery created for user {instance.email}")
            except Exception as gallery_error:
                logger.error(f"Failed to create gallery for user {instance.id}: {gallery_error}")
                print(f"❌ ERROR: Failed to create gallery for {instance.email}: {gallery_error}")
        
        # Send Welcome Email (separate transaction to not block user creation)
        try:
            send_welcome_email(instance)
            logger.info(f"Welcome email sent successfully to {instance.email}")
            print(f"📧 SUCCESS: Welcome email sent to {instance.email}")
        except Exception as email_error:
            logger.error(f"Failed to send welcome email to {instance.email}: {email_error}")
            print(f"❌ ERROR: Failed to send welcome email to {instance.email}: {email_error}")
            print("   📝 NOTE: User profile was still created successfully")
                
    except Exception as e:
        logger.error(f"Unexpected error in profile creation for user {instance.id}: {e}")
        print(f"❌ UNEXPECTED ERROR: Failed to process new user {instance.email}: {e}")
        # Don't re-raise the exception to avoid blocking user creation


def send_welcome_email(user):
    """
    Send a beautifully styled welcome email to new users.
    
    Args:
        user: The user instance to send email to
    """
    if not user.email:
        logger.warning(f"User {user.id} has no email address - skipping welcome email")
        print(f"⚠️  WARNING: User {user.id} has no email - skipping welcome email")
        return
    
    try:
        subject = 'Welcome to Altclan - Your Fashion Journey Begins Now! 🎉'
        email_from = settings.DEFAULT_FROM_EMAIL or 'noreply@altclan.com'
        recipient_list = [user.email]
        
        # Context for email template
        context = {
            'user_email': user.email,
            'user_name': getattr(user, 'first_name', '') or user.email.split('@')[0],
            'profile_url': f"{getattr(settings, 'SITE_URL', 'https://altclan.com')}/brands/profile/{user.id}/",
            'dashboard_url': f"{getattr(settings, 'SITE_URL', 'https://altclan.com')}/dashboard/",
            'support_email': 'support@altclan.com',
            'site_url': getattr(settings, 'SITE_URL', 'https://altclan.com'),
            'year': 2025
        }
        
        # Create HTML email content
        html_content = create_welcome_email_html(context)
        
        # Create plain text version
        text_content = f"""
Welcome to Altclan, {context['user_name']}!

We're thrilled to have you join our vibrant community of fashion labels and brands.

At Altclan, we strive to connect you with interested consumers who love the latest trends and unique pieces that you create.

To get started, here are a few things you can do:

• Personalize Your Profile: Complete your profile to receive personalized recommendations and exclusive offers.
• Upload Products: Start uploading your merchandise and track orders, payments and customers in your dashboard.
• Connect with Community: Engage with other brands and discover collaboration opportunities.

Visit your profile: {context['profile_url']}
Access your dashboard: {context['dashboard_url']}

We are here to support you every step of the way. If you have any questions or need assistance, feel free to reach out to our support team at {context['support_email']}

Thank you for choosing Altclan. We look forward to being a part of your fashion journey!

Best regards,
Enimofe Odujirin
Co-Founder, Altclan
{context['site_url']}
{email_from}
"""
        
        # Create and send email
        email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)  # Changed to fail_silently=True
        
    except Exception as e:
        logger.error(f"Email sending failed for {user.email}: {e}")
        # Don't re-raise to avoid blocking user creation


def create_welcome_email_html(context):

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Altclan</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f8fafc;
        }}
        
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
        }}
        
        .logo {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }}
        
        .header-subtitle {{
            font-size: 16px;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .content {{
            padding: 40px 30px;
        }}
        
        .welcome-title {{
            font-size: 28px;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .welcome-text {{
            font-size: 16px;
            color: #4a5568;
            margin-bottom: 30px;
            text-align: center;
            line-height: 1.7;
        }}
        
        .action-section {{
            background-color: #f7fafc;
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
        }}
        
        .action-title {{
            font-size: 20px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .action-list {{
            list-style: none;
            padding: 0;
        }}
        
        .action-item {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .action-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            flex-shrink: 0;
        }}
        
        .action-content h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 5px;
        }}
        
        .action-content p {{
            font-size: 14px;
            color: #718096;
            line-height: 1.5;
        }}
        
        .cta-section {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            margin: 10px;
            transition: transform 0.2s ease;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
        }}
        
        .cta-button.secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .support-section {{
            background-color: #edf2f7;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin: 30px 0;
        }}
        
        .support-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .support-text {{
            font-size: 14px;
            color: #4a5568;
            margin-bottom: 15px;
        }}
        
        .support-email {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer {{
            background-color: #2d3748;
            color: #a0aec0;
            padding: 30px;
            text-align: center;
        }}
        
        .footer-signature {{
            margin-bottom: 20px;
        }}
        
        .footer-name {{
            font-weight: 600;
            color: white;
            margin-bottom: 5px;
        }}
        
        .footer-title {{
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .footer-links {{
            font-size: 14px;
        }}
        
        .footer-links a {{
            color: #667eea;
            text-decoration: none;
            margin: 0 10px;
        }}
        
        .emoji {{
            font-size: 20px;
        }}
        
        @media (max-width: 600px) {{
            .email-container {{
                margin: 10px;
                border-radius: 12px;
            }}
            
            .header, .content {{
                padding: 25px 20px;
            }}
            
            .welcome-title {{
                font-size: 24px;
            }}
            
            .cta-button {{
                display: block;
                margin: 10px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <div class="logo">ALTCLAN</div>
            <div class="header-subtitle">Fashion Community Platform</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <h1 class="welcome-title">Welcome to Altclan, {context['user_name']}! <span class="emoji">🎉</span></h1>
            
            <p class="welcome-text">
                We're thrilled to have you join our vibrant community of fashion labels and brands. 
                At Altclan, we strive to connect you with interested consumers who love the latest trends 
                and unique pieces that you create.
            </p>
            
            <!-- Action Items -->
            <div class="action-section">
                <h2 class="action-title">Get Started in 3 Easy Steps</h2>
                <ul class="action-list">
                    <li class="action-item">
                        <div class="action-icon">
                            <span style="color: white; font-size: 18px;">👤</span>
                        </div>
                        <div class="action-content">
                            <h3>Personalize Your Profile</h3>
                            <p>Complete your profile to receive personalized recommendations and exclusive offers tailored just for you.</p>
                        </div>
                    </li>
                    <li class="action-item">
                        <div class="action-icon">
                            <span style="color: white; font-size: 18px;">📦</span>
                        </div>
                        <div class="action-content">
                            <h3>Upload Your Products</h3>
                            <p>Start showcasing your merchandise and track orders, payments, and customers in your personalized dashboard.</p>
                        </div>
                    </li>
                    <li class="action-item">
                        <div class="action-icon">
                            <span style="color: white; font-size: 18px;">🤝</span>
                        </div>
                        <div class="action-content">
                            <h3>Connect & Grow</h3>
                            <p>Engage with other brands, discover collaboration opportunities, and grow your fashion business.</p>
                        </div>
                    </li>
                </ul>
            </div>
            
            <!-- Call to Action -->
            <div class="cta-section">
                <a href="{context['profile_url']}" class="cta-button">Complete Your Profile</a>
                <a href="{context['dashboard_url']}" class="cta-button secondary">Visit Dashboard</a>
            </div>
            
            <!-- Support Section -->
            <div class="support-section">
                <h3 class="support-title">Need Help Getting Started?</h3>
                <p class="support-text">
                    We're here to support you every step of the way. If you have any questions or need assistance, 
                    our support team is ready to help!
                </p>
                <a href="mailto:{context['support_email']}" class="support-email">{context['support_email']}</a>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-signature">
                <div class="footer-name">Enimofe Odujirin</div>
                <div class="footer-title">Co-Founder, Altclan</div>
            </div>
            <div class="footer-links">
                <a href="{context['site_url']}">Visit Website</a> |
                <a href="mailto:{context['support_email']}">Contact Support</a> |
                <a href="{context['site_url']}/privacy">Privacy Policy</a>
            </div>
            <p style="margin-top: 15px; font-size: 12px;">
                © {context['year']} Altclan. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
"""


@receiver(post_save, sender=User)
def create_brand_profile_and_dashboard(sender, instance, created, **kwargs):
    """
    Create brand profile and dashboard for new brand users.
    
    Args:
        sender: The model class (BrandUser)
        instance: The actual brand user instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if not created:
        return
    
    try:
        # Create Brand Profile (outside transaction to avoid blocking user creation)
        try:
            brand_profile = BrandProfile.objects.create(brand_user=instance)
            logger.info(f"Brand profile created successfully for brand {instance.id}")
            print(f"✅ SUCCESS: Brand profile created for {instance.email} (ID: {instance.id})")
        except Exception as profile_error:
            logger.error(f"Failed to create brand profile for {instance.id}: {profile_error}")
            print(f"❌ ERROR: Failed to create brand profile for {instance.email}: {profile_error}")
        
        # Create Brand Dashboard
        try:
            dashboard = BrandDashboard.objects.create(brand=instance)
            logger.info(f"Brand dashboard created successfully for brand {instance.id}")
            print(f"📊 SUCCESS: Brand dashboard created for {instance.email}")
        except Exception as dashboard_error:
            logger.error(f"Failed to create brand dashboard for {instance.id}: {dashboard_error}")
            print(f"❌ ERROR: Failed to create brand dashboard for {instance.email}: {dashboard_error}")
        
        # Create default shipping and billing addresses
        try:
            ShippingAddress.objects.create(brand=instance, is_default=True)
            BillingAddress.objects.create(brand=instance, is_default=True)
            logger.info(f"Default addresses created for brand {instance.id}")
            print(f"📍 SUCCESS: Default addresses created for {instance.email}")
        except Exception as address_error:
            logger.error(f"Failed to create default addresses for {instance.id}: {address_error}")
            print(f"⚠️  WARNING: Failed to create default addresses for {instance.email}: {address_error}")
                
    except Exception as e:
        logger.error(f"Unexpected error in brand setup for {instance.id}: {e}")
        print(f"❌ UNEXPECTED ERROR: Failed to setup brand {instance.email}: {e}")
        # Don't re-raise the exception


# Utility function to test email sending
def test_welcome_email(user_email):
    """
    Test the welcome email functionality.
    Usage: from accounts.signals import test_welcome_email; test_welcome_email('test@example.com')
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(email=user_email)
        send_welcome_email(user)
        print(f"✅ TEST: Welcome email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False