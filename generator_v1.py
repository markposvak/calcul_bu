import random

def password_generator(length):
  alphabet = (
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '-/:;()$&@.,?!#%*+=_<>'
  )
  result = ''
  for i in range(length):
    symbol = random.choice(alphabet)
    result += symbol
  return


print(password_generator(10))
