import time
import jwt
import requests

def get_jwt_token(access_key, secret_key):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 1800,  # Valid for 30 minutes
        "nbf": int(time.time()) - 5
    }
    return jwt.encode(payload, secret_key, headers=headers)

def get_lip_sync_tasks(token, page_num=1, page_size=30):
    url = "https://api.klingai.com/v1/videos/lip-sync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "pageNum": page_num,
        "pageSize": page_size
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    # Your credentials
    access_key = "566a91f2b70d4c18b539d9d6ef91deb4"
    secret_key = "9c45d2addf0d490dab91e92b9777750f"
    
    # Get JWT token
    token = get_jwt_token(access_key, secret_key)
    
    # Get tasks
    result = get_lip_sync_tasks(token)
    
    # Print results
    if result.get("code") == 0:
        tasks = result.get("data", [])
        print(f"Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"Task ID: {task['task_id']}")
            print(f"Status: {task['task_status']}")
            print(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task['created_at']/1000))}")
            print("-" * 50)
    else:
        print(f"Error: {result.get('message')}")

if __name__ == "__main__":
    main()