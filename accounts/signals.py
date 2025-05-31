
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile
 
from .models import CustomUser
 
from brands.models import UserBillingAddress, BillingAddress
from django.core.mail import send_mail




User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Altclan'

        message = f"""
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
        email_from = 'noreply@altclan.com'
        recipient_list = [instance.email]
        
        Profile.objects.create(user=instance)
        print("New user profile has been created for ", instance.email)
        # send email to new user
        send_mail( subject, message, email_from, recipient_list )

 