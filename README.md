# KlingAI Video Pipeline Scripts

## Installation

```shell
cd `/the/folder/where/you/want/to/save/this/project`
```


```shell
git clone https://github.com/jeffhaskin/klingAPI-videoLipSycn.git
```


```shell
pip install requests pyjwt
```

## Usage

### Full Pipeline
The scripts can be used on one program to run the full `image --> video --> lip synced video` process all in one command:

```bash
python main.py
```


### Individual Steps
You can also run each step separately:

1. Create video:
```bash
python step1_image_to_video.py
```


2. Add lip sync (using video ID from step 1):
```bash
python step2_lip_sync.py
```


### Check Existing Task
```bash
python check_task.py
# Enter task ID when prompted
# Choose task type: 'image2video' or 'lip-sync'
```


## Configuration
Edit `config.py` to change:
- API credentials
- Model settings
- Input/output paths
- Timeout settings


🤖 AI Alert! This software was written by AI using Cascade Windsurfe and Claude 3.5 Sonnet.
