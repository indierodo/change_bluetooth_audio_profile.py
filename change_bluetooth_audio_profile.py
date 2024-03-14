# change_bluetooth_audio_profile.py

"""
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

"""

import time
import argparse
import subprocess

card_name = ''
device_address = ''
audio_profile_list = []

def cmd(cmd):
  """The ps.communicate() call will block until the process 
  finishes. It will return a tuple (stdout_data, stderr_data), 
  where stdout_data is the output of the process. Then we decode it 
  from bytes to a UTF-8 encoded string, and finally, we slice off 
  the newline ([:-1])."""
  ps = subprocess.Popen((cmd), stdout=subprocess.PIPE, shell=True)
  result = ps.communicate()[0].decode('utf-8')[:-1]
  # print(cmd, '\n', result)
  return result

def get_bluetooth_device_card_name():
  global card_name
  global device_address
  
  result = cmd('pactl list | grep "Name: bluez_card." | cut -d " " -f 2')
  card_name = result
  device_address = result[11:28].replace('_', ':')

def get_available_profiles():
  global audio_profile_list

  result = cmd('pactl list cards | awk -v RS="" "/bluez/"| sed -n "/Profiles/,/Active Profile/p"')
  lines = result.splitlines()[2:-1];
  for line in lines:
    audio_profile_list.append(line.split(':')[0].split('\t')[2])

def connected():
  result = cmd(f'bluetoothctl info {device_address} | grep Connected | cut -d " " -f 2')

  if result == 'yes':
    return True
  elif result == 'no':
    return False

def ask_for_audio_profile(): 
  global audio_profile_list
  
  for idx, profile in enumerate(audio_profile_list):
    print(idx+1, ': ', profile, sep='')

  user_choice = int(input('Select a profile: '))

  selected_audio_profile = audio_profile_list[user_choice - 1]

  set_audio_profile(selected_audio_profile)

def set_audio_profile(audio_profile):
  if audio_profile in audio_profile_list:
    cmd(f"pactl set-card-profile {card_name} {audio_profile}")
  else:
    print("Invalid profile")

def connect():
  cmd(f"bluetoothctl connect {device_address}")
  time.sleep(4)

def disconnect():
  cmd(f"bluetoothctl disconnect {device_address}")
  time.sleep(4)

def main(reconnect, profile):
  get_bluetooth_device_card_name()
  get_available_profiles()

  if reconnect == 'yes':
    if connected() == True:
      disconnect()
      connect()
  elif reconnect == 'no':
    pass
  else:
    print('Invalid arguments')
    return
  
  if (profile == "choose_myself"):
    ask_for_audio_profile()
  else:
    set_audio_profile(profile) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for changing the audio profile of a bluetooth device (PulseAudio)")
    parser.add_argument("--reconnect", default="no", choices=["yes", "no"], help="specify whether to reconnect the bluetooth device (yes/no)")
    parser.add_argument("--profile", default="choose_myself", help="specify the audio profile. Leave it blank to get a list of the available audio profiles.")
    
    args = parser.parse_args()

    main(args.reconnect, args.profile)
