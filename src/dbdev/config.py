import os
from dotenv import load_dotenv

load_dotenv()

def get_env(var, default=None):
    return os.getenv(var, default)
