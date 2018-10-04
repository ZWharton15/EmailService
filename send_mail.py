import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import zipfile
import os
from getpass import getpass

#Global parameters that are assigned when the script is imported and used to register with the SMTP
global sender_name
global sender_pass
global recipient


"""
Decorator to simplify the sending of emails in between the training of deep models or classifiers.

@param func: the function object that will be called in between the sending of emails.
@return: the function object that can be called to send emails and start the training of a specific model
"""
def training_mail_manager(func):
	def wrapper(*args, **kwargs):
		try:
			func(*args, **kwargs)
			print("Sending results")
			mail(subject="Python script complete", text="Well done. Attached are the results", attachment=args[-1])
		except Exception as e:
			print("Crashed: " + str(e))
			mail(subject="Python script has crashed", text=("Just a heads up. Heres the error message:\n" + str(e)))
	return wrapper


"""
Zips all the files given in the directory parameter, either as a list or a whole directory to be iterated.
@param zipped_name: the name that the zip file is given
@param directory: the path of the attachment file(s)
@param is_list: boolean value to determine if attachment is a list of files or a whole directory
@return: returns the full name of the zip file
"""
def zip_attachment(zipped_name, directory, is_list):
    print("zipping files")
    _zipfile = zipfile.ZipFile(zipped_name + ".zip", 'w', zipfile.ZIP_DEFLATED)
    #Itertate through a list
    if is_list:
        for fil in directory:
            _zipfile.write(fil)
    else: #Iterate through a directory
        for root, dirs, files in os.walk(directory):
            for fil in files:
                _zipfile.write(os.path.join(root, fil))
    
    #Close the connection to the zip file
    _zipfile.close()
    print("returning zip")
    return zipped_name + ".zip"

"""
Send an email from the logged in account to a single recipient.
@param subject: the string to be put as the email subject line
@param text: the text to be put in the main email content
@param attachment: optional parameter used to attach 1 or more files to the email. Either a list of files or a whole directory
"""
def mail(subject, text, attachment=None):
    #Create the structure for the email
    msg = MIMEMultipart()
    msg['From'] = sender_name
    msg['To'] = recipient
    msg['Subject'] = subject
    
    msg.attach(MIMEText(text,'plain'))
    
    #Check if there is an attachment to add
    clear_file = False
    if attachment != None:
        #check if there is more than 1 file to attach via a list or directory to zip
        if isinstance(attachment, list):
            print("is list of files")
            attachment = zip_attachment("output", attachment, is_list=True)
            clear_file = True
        elif os.path.isdir(attachment):
            attachment = zip_attachment("output", attachment, is_list=False)
            clear_file = True
        print("Attaching file")
        #Add the file or zipped folder
        file = open(attachment, "rb")
        part = MIMEApplication(file.read(), Name=basename(attachment))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
        msg.attach(part)

    #Create a connection to the email server
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.starttls()
    #Login using the senders detailed
    mailServer.login(sender_name, sender_pass)
    text = msg.as_string()
    #Send the email
    mailServer.sendmail(sender_name, recipient, text)
    mailServer.quit()
    
    print("email sent successfully")
    
    #remove the zipped folder if one was created 
    if clear_file:
        print("deleting zipped folder")
        del file
        os.remove(attachment)


#Make the user enter the sender and recipient details when this module is imported
if __name__ == "send_mail_decorator":
    #prompt user for email login
    sender_name = input("Enter senders email adderess: ")
    sender_pass = getpass("Enter senders password: ")
    recipient = input("Enter recipients email address: ")
	
    #Hide the account details
    clear = lambda: os.system('cls')
    clear()
    
    #Send an email to ensure the correct person will recieve the updates
    mail("Notification of login", "You will receive an email in the near future to inform you of the status of a your script.")
    