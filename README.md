# ATHack2020

### Install
install dependencies with
`pip3 install -r requirements.txt`

### Instructions
To open a window that accesses your webcam, run the following command:
`python3 video_window.py`

## Inspiration
We were inspired by our co-designer, Sue! She lives with retinal toxicity, which makes it very difficult to see things that don't have very much contrast (printed text, projected images and smartboards, etc), as it's hard to distinguish the edges. Sue asked us to help design and build a tool for adding contrast in real-time to the projected items she looks at. Sue hopes to use this tool to resume attending conferences, be able to participate in town meetings, resuming vocational goals, continuing coursework, with the goal of gainful employment. Sue is one of over 2 million Americans age 50 or older living with this condition that could benefit from this tool. 285 million people suffer from visual impairment worldwide.

## What it does
Our tool takes in an image from a  webcam, does image processing to enhance the image and add contrast, and displays the improved video stream on the computer of our user. It allows the user to pan or zoom in real time, adjust enhancement settings, and pause/save the video stream for easier access to projected video content.

## How we built it
We built this using PyQt for the user interface, OpenCV for the image processing, and a Logitech C922x Pro Stream camera for capturing the projected images. The co-designing process is reflected throughout the tool - various design decisions were tailored specifically for the needs of our co-designer. The larger font, black-and-white color theme, saveability of images, and the usability of the pan and zoom interfaces were a direct result of our conversations with Sue.

## Challenges we ran into
- Getting Pan/Zoom to work
- image quality (webcam couldn't really capture the text well enough, need a better camera to really make this useful)
- Deploying this onto multiple platforms (especially Windows, the OS that Sue uses) proved to be difficult

## Accomplishments that we're proud of
- Working product
- Tailored for the needs of Sue

## What we learned
- The importance of listening to your client's needs
- Hardware Limitations
- Deployment process can be difficult
- Copy/Paste from StackOverflow is a lifesaver


## What's next for ProClear
- Get it to deploy to multiple OS's
- Improve the quality of the images
