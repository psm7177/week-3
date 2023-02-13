from dotenv import load_dotenv   # dotenv 
import os                        # os 환경변수

load_dotenv()

mysql_connection_string = os.environ.get('MYSQL_CONNECTION_STRING')