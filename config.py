import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DB_URL = os.getenv("DB_URL")
REDIS_URL = os.getenv("REDIS_URL")
HELP_TEXT = (
    "При добавлении канала используйте адрес формата https:"
    "//www.youtube.com/@example или же само название"
    " в формате @example"
)
