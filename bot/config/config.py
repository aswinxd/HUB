import os
from dotenv import load_dotenv

load_dotenv("./.env")


class Config:
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "6350652136:AAFriDrVaXsIEchvLTj8BY3JEvvCGyVjTHI")
  BOT_NAME = os.environ.get("BOT_NAME", "erewew")

  API_ID = int(os.environ.get("API_ID", "12799559"))
  API_HASH = os.environ.get("API_HASH", "077254e69d93d08357f25bb5f4504580")

  DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://bot:bot@cluster0.8vepzds.mongodb.net/?retryWrites=true&w=majority")
  SESSION_NAME = os.environ.get("DATABASE_NAME", "Aleena")

  LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1001931553423))
  SUDO_USERS = [int(user) for user in (os.environ.get("SUDO_USERS","1137799257")).split()]
  SUPPORT_CHAT_URL = os.environ.get("SUPPORT_CHAT_URL", "https://t.me/subotsupport")
