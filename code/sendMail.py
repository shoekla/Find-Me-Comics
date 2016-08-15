import smtplib

def sendEmailFromAbir(sub, mess,name):
	to = name
	print "1"
	gmail_user = 'alanthehelper@gmail.com'
	print "2"
	gmail_pwd = 'aadi2247'
	print "3"
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	print "4"
	smtpserver.ehlo()
	print "5"
	smtpserver.starttls()
	print "6"
	smtpserver.ehlo
	print "7"
	smtpserver.login(gmail_user, gmail_pwd)
	print "8"
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:'+sub+' \n'
	print header
	msg = header + '\n'+mess+' \n\n'
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()

def send_mail(sub,message,name):

    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    gmailUser = 'alanthehelper@gmail.com'
    gmailPassword = 'aadi2247'
    recipient = name

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = sub
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()


#send_mail("Mail Test","")

