import string, random;

length = random.randint(1, 8)
alphabet = string.ascii_letters + string.digits
print(''.join([random.choice(alphabet) for i in range(length)]))