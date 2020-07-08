# NTUePoWatcher
## Introduction
Waiting for grades on NTU-eportfolio is so annoying. This script monitors changes on grade section of NTU e-portfolio. If changes have happened, an e-mail will be sent to notify user.

## Usage
``` 
python3 NTUePoWatcher.c
```
* In `main()`:
  * Set `epoUserName` to your user name for NTU e-portfolio (most likely your student ID). Your password would be prompted at running time.
  * Set `senderMail` to the gmail account you hope to send the notification e-mail from. Your password would be prompted at running time.
  * Set `receiverMail` to the gmail account you hope to receive the notification e-mail. This could be the same as `senderMail`, in which case the notification mail would be sent from you to yourself.
  * Set `timeInterval` to the time interval (in seconds) at which you hope `NTUePoWatcher` to check the grade section of NTU e-portfolio. Its value is set to be `10`. Please set its value to be at least 10 seconds, since there might be delay when requesting pages.


## Required Packages
* `requests 2.24.0`

## Note
* The script is only roughly tested on macOS.

