import random
import string
password_length = 6

def generate_password(ID=None, test=False):
    if test and ID!=None:
        return "test"+str(ID)[0]+str(ID)[2]
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(password_length))
