import requests
from config import API_CONFIG, TASK_CONFIG
from utils import get_auth_headers, wait_for_task, print_json, Timer

def create_video():
    timer = Timer()
    print("\n🎥 STEP 1: Creating Video from Image")
    print("\nℹ️ Using configuration:")
    print_json(TASK_CONFIG)
    
    url = f"{API_CONFIG['base_url']}/v1/videos/image2video"
    payload = {
        "model_name": TASK_CONFIG['model_name'],
        "mode": TASK_CONFIG['mode'],
        "duration": TASK_CONFIG['duration'],
        "image": TASK_CONFIG['image_url'],
        "prompt": TASK_CONFIG['prompt'],
        "negative_prompt": TASK_CONFIG['negative_prompt']
    }
    
    print("\n📤 Sending request to create video...")
    timer.start_segment('Queue Time')
    response = requests.post(url, headers=get_auth_headers(), json=payload)
    response.raise_for_status()
    
    print("\n📡 Initial API Response:")
    response_data = response.json()
    print_json(response_data)
    
    task_id = response_data['data']['task_id']
    print(f"\n📋 Task ID: {task_id}")
    
    result = wait_for_task(task_id, '/v1/videos/image2video', timer)
    
    if result['data']['task_status'] == 'failed':
        raise Exception(f"Video creation failed: {result['data'].get('task_status_msg')}")
    
    video_id = result['data']['task_result']['videos'][0]['id']
    print(f"\n✅ Video created successfully!")
    print(f"📼 Video ID: {video_id}")
    
    print("\n⏱️ Timing Report:")
    timer.print_segments()
    
    return video_id, timer

if __name__ == '__main__':
    video_id, _ = create_video()
    print("\n🎬 Final Video ID for next step:", video_id)