#!/bin/bash

# This is a simple script to set up the oem-setup.sh script to run on next
# boot. This is an in-between step to allow additional packages or 
# configurations to be made after the oem install. When that is finihsed,
# this script will be run to set up the install for the end user's first boot


zenity --question --title="Revenge OEM Install Setup" --text "When you are finished with any setup\nthat you would like to do, please select 'yes'. You may minimize this dialog, or even reboot as many times as needed.\nThis dialog will show on each reboot until 'yes' is selected.\nWhen you select 'yes', the setup for the end user\nwill start on the next boot.\n\nYou can now made any additional configurations or install any\nadditional software that you would like." --height=50

if [ $? = "1" ]
    then exit
fi

configure() {
mkdir -p /etc/systemd/system
cp -r /etc/oem-install/getty@tty1.service.d /etc/systemd/system/
cp /etc/oem-install/.bash_profile /root/
cp /etc/oem-install/.xinitrc /root/
cp /etc/oem-install/.xsession /root/
halt
}

configure
