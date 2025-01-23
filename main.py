from step1_image_to_video import create_video
from step2_lip_sync import create_lip_sync
from config import API_CONFIG
from utils import print_json, Timer
from playsound import playsound

def main():
    global_timer = Timer()
    print("\n🚀 Starting Lip Sync Video Creation Pipeline")
    print("\n🔐 Using API credentials:")
    print_json({
        "access_key": API_CONFIG['access_key'],
        "secret_key": f"{API_CONFIG['secret_key'][:8]}...{API_CONFIG['secret_key'][-8:]}",
        "base_url": API_CONFIG['base_url']
    })
    
    try:
        video_id, video_timer = create_video()
        final_url, lip_sync_timer = create_lip_sync(video_id)
        
        print("\n🎉 Process completed successfully!")
        print("🔗 Final video URL:", final_url)
        print("\n⚠️  Note: Video will be available for 30 days")
        
        print("\n📊 Final Timing Report:")
        print("\nVideo Generation:")
        video_timer.print_segments()
        print("\nLip Sync Generation:")
        lip_sync_timer.print_segments()
        print("\nTotal Process:")
        print(f"Global Time: {global_timer.get_total():.2f} seconds")
        
        playsound('/Users/jeffhaskin/Library/Mobile Documents/com~apple~CloudDocs/Business/Celerity/SOWs/SOW3/SOW3.1/Scripts/Assets/NewsTing.mp3')
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    main()