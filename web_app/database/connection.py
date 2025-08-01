import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")

database = os.getenv("DATABASE")
db = sqlite3.connect(database)