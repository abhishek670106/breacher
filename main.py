#breach checker bot with only two requests per 6 hour
import telegram
import telepot
import datetime
import requests
import json

# Set the API token
API_TOKEN = "5913440729:AAEjx5-7VEqaz9iTOvRS1EFIvXrpyoEv5OM"

# Create a dictionary to store the timestamp of the last request made by each user
last_request = {}

OWNER_LINK = "https://t.me/Abraham56780"

# Define the function to handle incoming messages
def handle_message(msg):
  # Get the chat ID and username of the sender
  chat_id = msg['chat']['id']
  username = msg['chat']['username']
  first_name = msg['chat']['first_name']

  # Get the message text
  text = msg['text']

  # Check if the message text is a command
  if text.startswith("/"):
    # Check which command was sent
    if text == "/start":
      # Send a message to the user with instructions

      bot.send_message(chat_id=chat_id, text=f"Hi {first_name},\n\n Welcome to Breach checker Bot.\n\nI can help to you find your breached password and the sorce of the breach.\n\n The bot is in beta stage . so You can only make two requests per 6 hours.\n\nCheck /help for more...")
    elif text == "/help":
      # Send a message to the user with help information
      keyboard = [[telegram.InlineKeyboardButton("Contact Admin", url=OWNER_LINK)]]
      reply_markup = telegram.InlineKeyboardMarkup(keyboard)
      bot.send_message(chat_id=chat_id, text=f"Hi {first_name},\n\nSend only your email address to check your are breached or not\n\n You can only make two requests per 6 hours. \n\nUse the /start command to see the instructions again .\n\n Click the button below to contact Admin.", reply_markup=reply_markup)
  else:
    # Check if the user has made two requests within the last 6 hours
    if username in last_request and len(last_request[username]) >= 2 and (datetime.datetime.now() - last_request[username][0]).total_seconds() < 21600:
      # Calculate the remaining time until the next request is allowed
      remaining_time = 21600 - (datetime.datetime.now() - last_request[username][0]).total_seconds()

      # Calculate the number of hours, minutes, and seconds remaining
      hours, remainder = divmod(remaining_time, 3600)
      minutes, seconds = divmod(remainder, 60)

      # Send a message to the user stating the remaining time until the next request is allowed
      bot.send_message(chat_id=chat_id, text=f"You have to wait {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds before making another request.")
    else:
      # Update the last request timestamp for the user
      if username in last_request:
        last_request[username].append(datetime.datetime.now())
      else:
        last_request[username] = [datetime.datetime.now()]

      # Split the message text into the two strings
      string = text
      print(string)
      inp = string
      # print(inp)
      url = "https://redacted.p.rapidapi.com/"
      querystring = {"func": "auto", "term": "someone@example.com"}
      querystring.update({"term": inp})
      headers = {
        "X-RapidAPI-Key": "c59dddda75mshc7a4cae73fca17ap1e5cc8jsn2fd0dcb9bc7f",
        "X-RapidAPI-Host": "redacted.p.rapidapi.com"
      }
      response = requests.request("GET", url, headers=headers, params=querystring)
      dataa = response.text
      print(dataa)
      if dataa.find('found') != -1:
        json_string = dataa
        json_object = json.loads(json_string)
        for result in json_object["result"]:
          password = result["password"]
          source = result['sources'][0]
          result_string = "The password for " + inp + " is " + password + " (source: " + source + ")"
          # print(result_string)
          a = str(result_string)
          # print(a)
          bot.send_message(chat_id=chat_id, text=a)
      elif dataa.find('message') != -1:
        bot.send_message(chat_id=chat_id, text="Contact the admin to update. api quota is exceeded")

      else:
        bot.send_message(chat_id=chat_id, text="The email address you provided was not found in any known data breaches.")

      # Concatenate the two strings and send the result back to the user


# Create the bot object
bot = telegram.Bot(token=API_TOKEN)

# Set the bot to handle messages
telepot.Bot(API_TOKEN).message_loop(handle_message)

print("Listening for messages...")

# Run the bot indefinitely
while True:
  pass
