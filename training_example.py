"""
A demonstation of how the decorator can be used in training
"""

from send_mail import training_mail_manager

def do_a_test():
	print("70% test accuracy")


def do_a_learn(model_name, output_dir):
	print("The model is: " + model_name)
	print("0% accuracy")
	print("50% accuracy")
	print("100% accuracy")
	do_a_test()

start = training_mail_manager(do_a_learn)

start("Inception", "D:/test1")
start("ResnetV2", "D:/test2")
start("VGG16", "D:/test3")


