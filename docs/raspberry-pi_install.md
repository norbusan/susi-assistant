# Installation on Raspbian Lite

- Tested on Raspberry Pi 3 with Raspbian Stretch Lite

## Configure before access

Assume that you don't have dedicated monitor and keyboard for your RPi. This is the first setup you need to do, to be able to access it later.

- Insert RPi SD card to your laptop.
- If you are using Ubuntu on laptop, the SD card should be mounted automatically.
- Go to the `boot` folder of SD card, put an empty file named _ssh_ there. This is to enable SSH.

```
sudo touch ssh
```
- Go to the `rootfs` folder of SD card. Edit the file _etc/wpa_supplicant/wpa_supplicant.conf_, to let RPi connect to your home wifi network later. The example content will be like this:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

country=VN

network={
        ssid="My warm home"
        psk="thisispassword"
}
```
- Now you can unmount, and unplug the SD card.

## Install SUSI Linux

- Install `git` on your RPi with this command `sudo apt-get install git`.
- Update your system using `sudo apt-get update && sudo apt-get upgrade `
- Clone repository and install dependencies
    - In your root directory, make a folder named `SUSI.AI` and move into the folder.
    - Clone the repository for SUSI Linux and move into the folder.
    ```
    $ mkdir SUSI.AI
    $ cd SUSI.AI
    $ git clone https://github.com/fossasia/susi_installer.git
    $ cd susi_installer
    ```
- Run the install script by running
    ```
    $ sudo ./install-requirements.sh --system-install --raspi
    $ sudo ./install.sh --clean
    ```
- Enjoy :smile:


# Installation on Raspbian with desktop

Tested on Raspberry Pi 3 with Raspbian Stretch.

You will need to have access to Raspberry Pi Screen and terminal for the initial setup.
You may start from ssh later.

The setup has been tested on Raspbian Jessie latest iso from Raspbian Website as on 31 July, 2017
Make sure you update your system before starting installation using
```
$ sudo apt update && sudo apt upgrade
```
Then install basic requirements
```
sudo apt-get install oracle-java8-jdk git
```


### IMPORTANT

- For installation of PocketSphinx on Python 3.4 (latest available on Raspbian Repositories), you need to change
system locale to ```en_US.UTF-8```. You may changes locale later after installation if you wish to.
Refer to this article for step by step instructions on changing locale to ```en_US.UTF-8```

    - http://rohankapoor.com/2012/04/americanizing-the-raspberry-pi/

    - You just need to change locale. Timezone and other changes illustrated in article are not needed.
- For installation on devices running on Armv6 processors (e.g. Raspberry Pi Zero / Zero W/ Zero WH/ 1A/ 1B):
    - Please use Java 8 (Either Oracle or OpenJDK).
        - For most debian based OS, including Raspbian, you may install OpenJDK's Java 8 JRE and JDK by running
        - `sudo apt install openjdk-8-jre* openjdk-8-jdk*`

## Steps

#### Clone repository and install dependencies
- In your root directory, make a folder named `SUSI.AI` and move into the folder.
- Clone the repository for SUSI Linux and move into the folder.
```
$ mkdir SUSI.AI
$ cd SUSI.AI
$ git clone https://github.com/fossasia/susi_installer.git
$ cd susi_installer
```
- Run the install script by running
```
$ ./install.sh
```

#### Configure Microphone and Speaker
- Connect your microphone and speaker to Raspberry Pi
- Open Menu > Preferences > Audio Device Settings.
![Audio Settings selection menu](./images/menu-audio-settings.png)
- In Audio Settings, select card bcm2835 and click on select controls button.
![bcm2835 selection](./images/bcm2835-no-controls.png)
- Tick on PCM option and close the dialog
![bcm2835 selection](./images/pcm-select.png)
- Now, select card for your microphone. Since, I am using a webcam with Microphone inbuilt it
is showing it as "USB 2.0 PC Camera". It can be different for your device.
![mic selection](./images/select-mic-card.png)
- Now click on select controls and then select the microphone control.
![mic control](./images/enable-mic.png)
- You may adjust input and output volume for your devices using sliders.
- Test your microphone working by running command ```rec a.wav``` (you need the 'sox' package for this). It should give an output like below.
![rec command](./images/rec-command.png)
- Test your speaker using play command. You may play the just recorded ```a.wav``` file using
```play a.wav``` command. It should give an output like below.
![play command](./images/play-command.png)

If you face an error in running above 2 commands, it is quite probable the PulseAudio is not running.
Start it by running the command
```pulseaudio -D```

### Optional Hardware Wake Button
![Wake Button](images/pi_button.jpg)

You may add an optional Push Switch to Wake Up SUSI without the need of speaking Hotword.
For enabling this, you need:
- A Push Switch
- Two Male to Female jumper Wires
- A Breadboard

#### Steps:
- Connect button to Raspberry Pi according to the following schematic diagram.

![Button Connection](images/connection.png)
- Install Raspberry Pi GPIO Python library: ```sudo -E pip3 install RPi.GPIO```
- While running the configuration script below, select the option to enable Hardware Button when
asked.

#### Configure and Run SUSI Linux

Several executables are installed into `~/SUSI.AI/bin`, in particular
`susi-config` (configuration utility), `susi-linux start` (headless start),
and `susi-linux-app` (GUI app).

- Run the SUSI configuration script. This will allow you to customize the
setup according to your needs. It can be used to modify:
    - TTS service
    - Speech Recognition service
    - Authenticate to SUSI.AI
    - Enable Hardware Wake Button.

Install required python libraries:
```
$ pip3 install json_config
$ pip3 install service_identity
```    
Run the script using:
```
$ susi-config set stt=<stt> tts=<tts> hotword=<hotword> wakebutton=<enable|disable>
$ susi-config set susi.mode=<choice> susi.user=<email> susi.pass=<pass>
```
- Once configured, you may run SUSI User Interface by executing the following command
```
$ susi-linux-app
```
- Alternatively ,you can run SUSI without User Interface by executing the following command
```
$ susi-linux start
```
In both case SUSI will start in always listening Hotword Detection Mode. To ask SUSI a question, say "Susi". If detection of
hotword is successful, you will hear a small bell sound. Ask your query after the bell sound. Your query will be
processed by SUSI and you will hear a voice reply.

If you have additionally enabled the Wake Button, you may press the button anytime to invoke SUSI. You will hear a small
bell after pressing button to confirm SUSI has started listening. Ask your query after that.

#### Faced any errors?

If you still face any errors in the setup, please provide a screenshot or logs of errors being encountered.
This would help rectify the issue.
