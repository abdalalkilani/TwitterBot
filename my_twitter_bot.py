import tweepy
import time
import random
import requests
from bs4 import BeautifulSoup

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

print("AYOO")


giphy_api_key = "giphy_api_key"

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_KEY = 'ACCESS_KEY'
ACCESS_SECRET = 'ACCESS_SECRET'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

mentions = api.mentions_timeline()

def binary_search(a, x):
    lo = 0
    hi = len(a)

    while lo < hi:
        mid = (lo + hi) // 2
        print(open(a[mid]).read())
        if not x in open(a[mid]).read():
            lo = mid + 1
        elif x in open(a[mid]).read():
            hi = mid
        elif mid > 0 and x in open(a[mid-1]).read():
            hi = mid
        else:
            return mid

    return -1

def binary_search1(arr, low, high, x):

  with open(arr) as f:
      lines = f.read().splitlines()
    # Check base case
      if high >= low:
          print("high", high)
          print("low", low)

          mid = (high + low) // 2
          print("mid", mid)
          print(lines[mid])
          print(x)
          # If element is present at the middle itself
          if lines[mid].lower() == x:
              return lines[mid]

          # If element is smaller than mid, then it can only
          # be present in left subarray
          elif lines[mid].lower() > x:
              return binary_search1(arr, low, mid - 1, x)

          # Else the element can only be present in right subarray
          else:
              return binary_search1(arr, mid + 1, high, x)

      else:
          # Element is not present in the array
          return -1

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def file_length(fname):
    lines = open(fname).read().splitlines()
    return len(lines)

def set_line(index, fname):
    lines = open(fname).read().splitlines()
    return lines[index]

def isSubsequence(self, s: str, t: str) -> bool:
    string = ''
    if len(s) == 0:
        return True
    for i in range(0,len(t)):
        if len(string) <= len(s)-1:
            if s[len(string)] == t[i]:
                string += s[len(string)]
    return s == string

FILE_NAME = 'last_seen_id.txt'

#Stores the last seen id so it knows what to respond to next, instead of responding to everything previously posted
#1568686429374664704
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def weather(city_name):
    print(city_name)
    api_key = "OpenWeatherMap API KEY"  # API key from the OpenWeatherMap website
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name  # This is to complete the base_url, you can also do this manually to checkout other weather data available
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        current_temperature = round(y["temp"] - 273.15, 2)

        farenheit = round(1.8*(y["temp"] - 273.15) + 32, 2)

        current_feels_like = round(y["feels_like"] - 273.15, 2)

        farenheit_like = round(1.8*(y["feels_like"] - 273.15) + 32, 2)

        current_pressure = y["pressure"]

        current_humidity = y["humidity"]

        z = x["weather"]

        weather_description = z[0]["description"]

        city = city_name+" weather"
        city = city.replace(" ", "+")

        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')

        location = soup.select('#wob_loc')[0].getText().strip()

        return( location +
                "\n" "Temperature = " +
                str(current_temperature) + "ºC " +
                "(" + str(farenheit) + "ºF" + ")" +
                "\n" "Feels like = " +
                str(current_feels_like) + "ºC " +
                "(" + str(farenheit_like) + "ºF" + ")" +
                "\n" "Humidity = " +
                str(current_humidity) + "%" +
                "\n" "Pressure = " +
                str(current_pressure) + " hPa" +
                "\n" "Description = " +
                str(weather_description))

    else:
        return(" City Not Found ")

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
        # NOTE: We need to use tweet_mode='extended' below to show
        # all full tweets (with full_text). Without it, long tweets
        # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if isSubsequence(isSubsequence, 'respond', mention.full_text.lower()):
            print('found RESPOND!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' Hello, Whats up?', mention.id)
        if isSubsequence(isSubsequence, 'quote', mention.full_text.lower()):
            print('found QUOTE!', flush=True)
            print('sending quote...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' +
                    random_line('quote_file.txt'), mention.id)
        if 'weather' in mention.full_text.lower():
            city_name = 'NOT FOUND'
            print(set_line(1, 'city_names.txt'))
            length = file_length('city_names.txt') - 1
            lastword = ""
            for i in mention.full_text.lower().split():
                print(i)
                if i == "@dulsterbot" or i == "weather" or i == "in" or i == "what" or i == "whats" or i == "is":
                    pass
                else:
                    if i == "random":
                        city_name = random_line('city_names.txt')
                        break
                    binary_result = binary_search1('city_names.txt',0, length, i)
                    print(binary_result)
                    if binary_result != -1:
                        city_name = binary_result
                        break
                    else:
                        doublecity = lastword + " " + i
                        binary_result = binary_search1('city_names.txt',0, length, doublecity)
                        if binary_result != -1:
                            city_name = binary_result
                            break
                    lastword = i

            print('found CITY!', flush=True)
            print('sending weather data...', flush=True)
            print(weather(city_name))
            api.update_status('@' + mention.user.screen_name + ' ' +
                    weather(city_name), mention.id)
        for compliment in range(0, file_length('compliment_msg.txt')):
            if set_line(compliment, 'compliment_msg.txt') in mention.full_text.lower():
                print('found COMPLIMENT!', flush=True)
                print('sending thanks...', flush=True)
                api.update_status('@' + mention.user.screen_name + ' ' +
                        random_line('compliment_replies.txt'), mention.id)
        for cheering_up in range(0, file_length('cheering_up_msg.txt')):
            if set_line(cheering_up, 'cheering_up_msg.txt') in mention.full_text.lower():
                print('found CHEERING UP!', flush=True)
                print('sending cheering up...', flush=True)
                api.update_status('@' + mention.user.screen_name + ' ' +
                        random_line('cheering_up_replies.txt'), mention.id)


def random_quote():
    print('sending HOURLY QUOTE', flush=True)
    api.update_status(random_line('quote_file.txt'))

def follow_for_follow():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

follow_for_follow()
while True:
    reply_to_tweets()
    time.sleep(15)
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    print(current_hour)
    current_minute = time.strftime("%M", t)
    print(current_minute)
    current_second = time.strftime("%S", t)
    print(current_second)
    if int(current_hour) == 9 and int(current_minute) == 0 and int(current_second) <= 15:
        random_quote()
