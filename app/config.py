import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    CHROMA_PATH: str = os.path.join(BASE_DIR, "chroma_db", "chroma_db")
    COLLECTION_NAME: str = "docs"
    LM_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    HF_MODEL_NAME: str = "deepseek-ai/DeepSeek-R1"  
    HF_MODEL_NAME_2: str = "Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24"  
    HF_API_TOKEN: SecretStr
    SECRET_KEY: str
    USERS: str = os.path.join(BASE_DIR, "users.json")
    ALGORITHM: str
    MAX_CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Config()  