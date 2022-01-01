import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "justin.wrightgrounds@gmail.com"
pas = "zwwuyvjhrptjhugv"

sms_gateways = ['5039361112@txt.att.net','503438-8825@msg.fi.google.com']

# The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
# and port is also provided by the email provider.
smtp = "smtp.gmail.com" 
port = 587
# This will start our email server
server = smtplib.SMTP(smtp,port)
# Starting the server
server.starttls()
# Now we need to login
server.login(email,pas)

# Now we use the MIME module to structure our message.
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = ", ".join(sms_gateways)
# Make sure you add a new line in the subject
msg['Subject'] = "Power outage has occured\n"
# Make sure you also add new lines to your body
body = "The power has failed\n"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email,sms_gateways,sms)

# lastly quit the server
server.quit()