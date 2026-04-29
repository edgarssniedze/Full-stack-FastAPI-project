from dotenv import load_dotenv
import os

load_dotenv()

def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

expire_min = int(get_env("ACCESS_TOKEN_EXPIRE_MIN", "30"))
secret_key = get_env("SECRET_KEY")
algorithm = get_env("ALGORITHM", "HS256")


