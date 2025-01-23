import requests
from config import API_CONFIG
from utils import get_auth_headers, wait_for_task, print_json
from playsound import playsound

def check_task(task_id, task_type):
    print(f"\n🔍 Checking status for task: {task_id}")
    print(f"📋 Task type: {task_type}")
    
    endpoint = f'/v1/videos/{task_type}'
    try:
        result = wait_for_task(task_id, endpoint)
        
        if result['data']['task_status'] == 'succeed':
            if task_type == 'image2video':
                video_id = result['data']['task_result']['videos'][0]['id']
                print(f"\n✅ Task completed successfully!")
                print(f"📼 Video ID: {video_id}")
            else:  # lip-sync
                video_url = result['data']['task_result']['videos'][0]['url']
                print(f"\n✅ Task completed successfully!")
                print(f"🎞️ Video URL: {video_url}")
            
            playsound('/Users/jeffhaskin/Library/Mobile Documents/com~apple~CloudDocs/Business/Celerity/SOWs/SOW3/SOW3.1/Scripts/Assets/NewsTing.mp3')
        else:
            print(f"\n❌ Task failed: {result['data'].get('task_status_msg', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error checking task: {str(e)}")
        raise

if __name__ == '__main__':
    task_id = input("Enter task ID: ")
    while True:
        task_type = input("Enter task type (image2video/lip-sync): ").lower()
        if task_type in ['image2video', 'lip-sync']:
            break
        print("Invalid task type. Please enter either 'image2video' or 'lip-sync'")
    
    result = check_task(task_id, task_type)
    print("\n📡 Final API Response:")
    print_json(result)