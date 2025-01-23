import requests
from config import API_CONFIG, TASK_CONFIG
from utils import get_auth_headers, wait_for_task, print_json, Timer

def create_lip_sync(video_id):
    timer = Timer()
    print("\n🎤 STEP 2: Creating Lip Sync Video")
    
    payload = {
        "input": {
            "video_id": video_id,
            "mode": "audio2video",
            "audio_type": "url",
            "audio_url": TASK_CONFIG['audio_url']
        }
    }
    
    print("\n📝 Request payload:")
    print_json(payload)
    
    url = f"{API_CONFIG['base_url']}/v1/videos/lip-sync"
    print("\n📤 Sending request to create lip sync...")
    
    response = requests.post(url, headers=get_auth_headers(), json=payload)
    response.raise_for_status()
    
    print("\n📡 Initial API Response:")
    response_data = response.json()
    print_json(response_data)
    
    task_id = response_data['data']['task_id']
    print(f"\n📋 Task ID: {task_id}")
    
    result = wait_for_task(task_id, '/v1/videos/lip-sync', timer)
    
    if result['data']['task_status'] == 'failed':
        raise Exception(f"Lip sync failed: {result['data'].get('task_status_msg')}")
    
    final_url = result['data']['task_result']['videos'][0]['url']
    print(f"\n✅ Lip sync created successfully!")
    print(f"🎞️ Final video URL: {final_url}")
    
    print("\n⏱️ Timing Report:")
    timer.print_segments()
    
    return final_url, timer

if __name__ == '__main__':
    video_id = input("\n🎬 Enter video ID from step 1: ")
    final_video_url, _ = create_lip_sync(video_id)