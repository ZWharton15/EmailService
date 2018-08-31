from sendMail import mail


#Calling the email method both in a successful completion and a crash to demonstrate the use of the email system
try:
    print("Sending mail")
    mail(subject="Python Script complete", text="Well done.")
except KeyboardInterrupt:
    print("Program stopped by keyboard interrupt")
except Exception as e:
    print("Crashed: " + str(e))
    mail(subject="Python Script has crashed", text=("Just a heads up. Heres the error message:\n" + str(e)))