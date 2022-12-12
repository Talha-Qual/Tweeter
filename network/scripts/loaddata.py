from network.models import Tweet, User, Profile
import csv

def create_user():
  username = 'Rick Astley'
  email = 'RickAstley@gmail.com'
  tw_handle = 'ricky'
  password = 'redrover'
  # Attempt to create new user
  try:
      user = User.objects.create_user(username, email, password)
      user.save()
      Profile.objects.create(user = user, handle = tw_handle)
  except:
    print("error")

def run():
  create_user()
  curr_user = User.objects.get(username = 'Rick Astley')
  with open('network/tweet_data.csv') as file:
      reader = csv.reader(file)
      next(reader)  # Advance past the header
      for row in reader:
          Tweet.objects.create(user = curr_user, tweet = row[1])