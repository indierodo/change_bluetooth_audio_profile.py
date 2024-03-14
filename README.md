# change_bluetooth_audio_profile.py
Script for changing the audio profile of a bluetooth device (PulseAudio)

I created this script to workaround a simple issue with my headphones,

I sometimes need to change the audio profile just after connecting, 
and the GUI failed to do it properly.

By running this script, it will automatically detect the available
audio profiles so you can choose one, or you can pass the profile
name as an argument.

usage: change_bluetooth_audio_profile.py [-h] [--reconnect {yes,no}] [--profile PROFILE]

Script for changing the audio profile of a bluetooth device (PulseAudio).

options:
  -h, --help            show this help message and exit
  --reconnect {yes,no}  specify whether to reconnect the bluetooth device (yes/no)
  --profile PROFILE     specify the audio profile. Leave it blank to get a list of the available audio profiles.
