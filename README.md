# Automate Mixdown initialization

A script that transfers all the VSTs on your MIDI tracks to a new track so you can freeze your MIDI tracks and then copies the VSTs back over for you and deletes the new tracks <br/>

## Setup:

1. Copy paste the downloaded/cloned repository in your Remote Scripts folder. Refer to the link to find out where the folder is for your OS:
https://help.ableton.com/hc/en-us/articles/206240184-Creating-your-own-Control-Surface-script

3. Select "ableton-mixdown-automation" in Preferences > Link/MIDI

4. Go to: 127.0.0.1:5010 or localhost:5010 in your browser and follow the instructions

## Note
It cannot freeze and flatten your tracks automatically as the Ableton API does not allow that.<br/>
Tested on Ableton 10.1.18 on Windows. I welcome contributions and/or issues so I can also adapt it for OSX/Ableton 11 if it does not work without changes.
The web interface sucks but does the job lol<br/>
**Errors**? **Wanna debug**? Check log.txt or see the code, it's very straightforward.

## LICENSE
GPL-3.0

#### Contributions, feedback and suggestions welcome. 
