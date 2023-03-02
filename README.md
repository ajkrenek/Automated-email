# Automated-email
This is a program that sends a daily personalized email embedded with a post and link from tumblr and image from a subreddit. This program also sends an anniversary email and displays the length since the anniversary date.


# Creating Reddit client_id and client_secret

Go to your Reddit account -> preferences -> apps. Create another app, give the bot a name and description. Select the script option and fill in about and redirect to anything. The client id and client secret values will be given to you. Fill in those values and the reddit username and password in the respective boxes.

# Creating app password for gmail
If you're using a gmail account to send emails, third party apps are no longer supported to access gmail, you will need to create an app password to allow Python to access the email account.
  1) Go to your gmail account -> Manage your Google account -> Security tab -> Scroll down and enable 2-Step Verification under 'Signing in to Google'.
  2) Go back to the Security Tab and underneath 2-Step Verification will be an 'App Passwords' tab, click that and generate an app password.
  
