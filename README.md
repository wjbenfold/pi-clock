# pi-clock

An alarm clock running on a raspberry pi zero.

## Usage

From base directory of repo:

`python src/start.py`

### Dependencies

* `flask`

## Features

* Play music at the alarm time
* JSON config with preset config options and daily schedule
* `running.flg` present when service is running
* `exit.flg` will stop the service
* Local http server to show alarm time
* Alarm time changing from UI (make new configs, choose config used by schedule)

## To do

* Either
    * Notify user of alarm time
    * Remotely unset the alarm
* Or
    * Local trigger to set alarm (e.g. beep on PIR trigger)
* Remote switch to set/cancel alarm
* Screen only turns on when needed / turns off when not needed
* Remote switch can trigger seeing the time briefly
