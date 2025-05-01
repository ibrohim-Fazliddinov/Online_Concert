from pydantic_settings import BaseSettings
import logging

from settings.path import PathSettings

env = PathSettings.env_path


logeer = logging.getLogger(__name__)

class Settings(BaseSettings):


    TITLE: str = "Online_Concert"
    DESCRIPTION: str = "CONCERT.RU CLONE"
    VERSION: str = '0.0.1'
    HOST: str = "0.0.0.0"
    PORT: str = "8000"

