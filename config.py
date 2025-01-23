API_CONFIG = {
    'access_key': 'YOUR_KLING_ACCESS_KEY',
    'secret_key': 'YOUR_KLING_SECRET_KEY',
    'base_url': 'https://api.klingai.com',
    'max_attempts': 60,  # Maximum number of status check attempts
    'check_interval': 10  # Seconds between status checks
}

TASK_CONFIG = {
    'image_url': '/link/to/avatar.png',
    'audio_url': '/link/to/voice-isoclated-song.wav',
    'duration': '10',
    'model_name': 'kling-v1-6',
    'mode': 'pro',
    'prompt': 'Beautiful young woman on a pop concert stage smiling while looking at the camera wearing sparkly black dress. lights, stage, audience. arms down, dancing, still camera, happy, medium close shot, concert documentary style, high definition, 4k, photo-real, mouth closed',
    'negative_prompt': 'disfigurement, low quality, scan lines, grainy, bad anatomy, microphone, camera movement'
}