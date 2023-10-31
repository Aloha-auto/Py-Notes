import time
import requests

current_time = time.strftime("%H:%M:%S", time.localtime(time.time() + 3600))

requests.post("https://ntfy.sh/alois-test-pc", 
              data=f"Test Successful - {current_time}")
