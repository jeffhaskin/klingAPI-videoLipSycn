import time
import jwt
import json
import requests
from config import API_CONFIG

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.segment_start = self.start_time
        self.segments = {}
        self.current_segment = None

    def start_segment(self, name):
        self.segment_start = time.time()
        self.current_segment = name

    def end_segment(self):
        if self.current_segment:
            self.segments[self.current_segment] = time.time() - self.segment_start
            self.current_segment = None

    def get_total(self):
        return time.time() - self.start_time

    def print_segments(self):
        for name, duration in self.segments.items():
            print(f"{name}: {duration:.2f} seconds")
        print(f"Total Time: {self.get_total():.2f} seconds")

def print_json(data):
    print(json.dumps(data, indent=2))

def generate_token(access_key, secret_key):
    headers = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    token = jwt.encode(payload, secret_key, headers=headers)
    print(f"\n🔑 Generated JWT Token:\n{token[:50]}...{token[-50:]}")
    return token

def get_auth_headers():
    token = generate_token(API_CONFIG['access_key'], API_CONFIG['secret_key'])
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

def wait_for_task(task_id, endpoint, timer=None, max_attempts=API_CONFIG['max_attempts'], delay=API_CONFIG['check_interval']):
    headers = get_auth_headers()
    attempt = 0
    auth_retries = 0
    max_auth_retries = 3
    
    while attempt < max_attempts:
        attempt += 1
        print(f"\n⏳ Checking task status (attempt {attempt}/{max_attempts})...")
        
        try:
            response = requests.get(
                f"{API_CONFIG['base_url']}{endpoint}/{task_id}",
                headers=headers
            )
            data = response.json()
            
            print("📡 API Response:")
            print_json(data)
            
            if data.get('code') == 1004:  # Auth failed
                if auth_retries < max_auth_retries:
                    auth_retries += 1
                    print(f"\n🔄 Auth failed, regenerating token (retry {auth_retries}/{max_auth_retries})")
                    headers = get_auth_headers()
                    attempt -= 1  # Don't count this as a task check attempt
                    continue
                else:
                    raise Exception("Max auth retry attempts exceeded")
            
            if data.get('code') != 0:
                raise Exception(f"API Error: {data.get('message')}")
            
            if data.get('data') is None:
                raise Exception("No data in API response")
                
            status = data['data']['task_status']
            print(f"\n📊 Current Status: {status}")
            
            if status == 'processing' and timer and 'Queue Time' in timer.segments:
                timer.end_segment()
                timer.start_segment('Generation Time')
            
            if status in ['succeed', 'failed']:
                if timer:
                    timer.end_segment()
                return data
                
            print(f"Waiting {delay} seconds before next check...")
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            print(f"\n⚠️ Network error: {str(e)}")
            time.sleep(delay)
            continue
    
    raise TimeoutError(f"Task {task_id} did not complete within timeout")