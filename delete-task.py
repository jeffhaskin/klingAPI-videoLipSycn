import jwt
import time
import requests
import json

def get_jwt_token(access_key, secret_key):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    return jwt.encode(payload, secret_key, headers=headers)

def delete_task(token, task_id):
    url = f"https://api.klingai.com/v1/videos/lip-sync/{task_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    print(f"\nSending DELETE request to: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.delete(url, headers=headers)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.text:
            return response.json()
        return {"error": "Empty response"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON in response: {response.text}"}

def main():
    access_key = "566a91f2b70d4c18b539d9d6ef91deb4"
    secret_key = "9c45d2addf0d490dab91e92b9777750f"
    
    task_id = input("Enter task ID to delete: ")
    token = get_jwt_token(access_key, secret_key)
    
    result = delete_task(token, task_id)
    print("\nDelete Response:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()