from twython import Twython
from twython import TwythonStreamer
from auth import (
    consumer_key, consumer_secret, access_token, access_token_secret
)


# Listens out for things
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            username = data['user']['screen_name']
            tweet = data['text']
            print("@{}: {}".format(username, tweet))


#stream = MyStreamer(
 #   consumer_key,
 #   consumer_secret,
 #   access_token,
 #   access_token_secret
#)

# stream.statuses.filter(track='raspberry pi')
# Listens for the track keyword and on success prints out the
# Screen Name and full text

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
# Uses the API's update_status() function to send a tweet containing hello twitter
#message = "Hello Josh, I'm watching you!"
#twitter.update_status(status=message)
#print("Tweeted: %s" % message)
def tweet (message):
    twitter.update_status(status=message)
# Code to upload image to Twitter
# image = open('image.jpg', 'rb')  # file opens the image
# response = twitter.upload_media(media=image)
# media_id = [response['media_id']]
# twitter.update_status(status=message, media_ids=media_id)
