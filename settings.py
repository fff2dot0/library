from os import environ
from dotenv import load_dotenv

load_dotenv( "./.env" )
URL     = environ[ "url" ]
LOGIN   = environ[ "login" ]
PWD     = environ[ "pwd" ]
