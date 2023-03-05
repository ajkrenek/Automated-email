# Automated-email
## This script sends a daily personalized email embedded with a post and link from tumblr and image from a subreddit. You can also send a custom email on a specified date, such as an anniversary.

In order for this script to run you will need to set up the following:
- Tumblr API 
- Reddit API 
- Gmail third party access

# Accessing Tumblr API
1. First you need to create a [tumblr account](https://www.tumblr.com/).
2. Once registered, you will then need to register your [app](https://www.tumblr.com/oauth/apps).
3. Once you have registered your application, you will be given an API key. Add the keys to the config.json file.
4. To make API requests, you will need to authenticate your requests using OAuth. You can find detailed instructions on how to do this in the Tumblr API documentation.

# Creating Reddit client_id and client_secret
1. First you will need to create a Reddit [account](https://www.reddit.com/).
2. Go to your [Reddit account -> preferences -> apps](https://www.reddit.com/prefs/apps/). 
3. Create another app, give the bot a name and description. 
4. Select the script option and fill in about and redirect to anything. 
5. The client id and client secret values will be given to you. Fill in those values and the reddit username and password in the respective boxes.
6. Add the tokens to config.json

# Creating app password for gmail
If you're using a gmail account to send emails, third party apps are no longer supported to access gmail; you will need to create an app password to allow the Python script to access the email account.
 1. Go to your gmail account -> Manage your Google account -> Security tab -> Scroll down and enable 2-Step Verification under 'Signing in to Google'.
 2. Go back to the Security Tab and underneath 2-Step Verification will be an 'App Passwords' tab, click that and generate an app password.

# Running the script
To run the script, you create an email class object with the following arguments:
- email -> This is the email address that the script will be accessing to send the emails from.
- passowrd -> This is the app password that the script will you use to login.
- to_email -> The email recipient.
- subject -> Subject header for the email.
- send_time -> The time that you would like to send emails at daily (must be in military time e.g. 3:00 pm = 15:00).
- ann_year -> The year that the recipient joined the email list/anniversary year
- ann_month -> The month that the recipient joined the email list/anniversary month
- ann_day -> The day that the recipient joined the email list/anniversary day
- tumblr_search_query -> A list of search queries that will be used to find posts.
- subreddit_list -> A list of subreddits that will be used to pull images from.
- port -> The port address of your email service (For Gmail the port is 465).

The email is structured using HTML and a basic template is provided, but can customized.
```

```

### ann_date function
The ann_date function calculates the years and months since the user joined the email list/anniversary date to display in the email on their anniversary date.

### tumblr_post function
The tumblr_post function picks a search query and searches for new posts, picking a random blog name. Then using the Tumblr API, it grabs a post from that blog, and embeds it into the email.
