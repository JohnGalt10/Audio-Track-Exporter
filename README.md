# Audio-Track-Exporter
An addon for Blender that exports each VSE channel containing audio strips as individual audio files to use for mixing and mastering in an external DAW. Made this for personal use and decided to publish it in case someone else finds it useful. 

_IMPORTANT NOTES:_
a. I won't be developing this script further with new features or updates
b. This script was tested using Linux with Blender 3.6 (Flatpak) only. So it may or may not work with your setup.
c. If you want to edit the script further for whatever reason, I just ask that you notify me so I can use it too


**Instructions:**
![Addon_Instructions](https://github.com/JohnGalt10/Audio-Track-Exporter/assets/138226393/45a380d0-f536-45dc-802d-5f60370d3b6f)

0. Organize the strips in your VSE channels so that all _audio_ files/strips sit on channels with no other files type on it (video, images, scenes, etc.). In the screenshot all video/images are on the first channel while the second and third channels are reserved for only audio files.
1. Set the file path for the outputted audio files by clicking on the folder icon on the right.
2. Adjust the slider to set the sample rate of the outputted files in Hz.
3. Choose the desired file type for your audio files to be exported in. Currently only options are FLAC and MP3 files.
4. Make sure the start and end markers are set correctly. These determine the start and end points of the exported audio files.
5. Click the Export button to render out the audio channels to individual files. A notification will display at bottom of Blender saying the export is completed.
6. Double check that the channels exported correctly to the specified file path.
