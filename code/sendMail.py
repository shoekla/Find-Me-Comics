import requests
def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb0f496f19f04499e9bbd0bf3e9001cfb.mailgun.org/messages",
        auth=("api", "key-73889882b06301ba156c2cf03441714d"),
        data={"from": "Find Me Comics <postmaster@sandboxb0f496f19f04499e9bbd0bf3e9001cfb.mailgun.org>",
              "to": "abirshukla@gmail.com",
              "subject": "Hello Abir Shukla",
              "text": "Congratulations Abir Shukla, you just sent an email with Mailgun!  You are truly awesome!  You can see a record of this email in your logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this sandbox server.  Next, you should add your own domain so you can send 10,000 emails/month for free."})


send_simple_message()    


