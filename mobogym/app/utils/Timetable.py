import datetime
import re
from django.utils.html import strip_tags
import math


def count_words(html_string):

    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)

    return count



def get_read_time(html_string):
    count = count_words(html_string)

    # Assume 200 words per min reading
    # Round Up
    read_time_min = math.ceil(count / 200.0) 
    # Round Down
    # read_time_min = math.floor(count / 200.0) 
    # read_time_sec = read_time_min * 60

    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = str(datetime.timedelta(minutes=read_time_min))

    Rs = ''
    tmp = read_time.split(':')
    j = ['Hour', 'Minute', 'Sec']
    for i in tmp:
        if int(i) != 0:
            Rs += str(int(i)) + ' ' + j[tmp.index(i)] + ('s' if int(i) > 1 else '') + ' '

    return Rs






# html = '''
# <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod<br />
# tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,<br />
# officia deserunt mollit anim id est laborum.</p>
# <p>Lorem ipsum dolor s

# '''

# tmp = get_read_time(html)

# print(tmp)

