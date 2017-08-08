#!/bin/bash

# this is a simple setup script for configuring Revenge OS
# after an OEM install.

title="Revenge OS OEM Setup"
logo="revenge_logo_sm.png"

config1() {
locales=$(cat /etc/locale.gen | grep -v "#  " | sed 's/#//g' | sed 's/ UTF-8//g' | grep .UTF-8 | sort | awk '{ printf "!""\0"$0"\0" }')

zones=$(cat timezone)

yad --width=600 --height=400 --center --title="$title" --image="$logo" --text "<big>Revenge Setup</big>\n\nEnter the following to set up your system:" --form --field="Select Your Keyboard Layout:":CB --field="Select Your locale:":CB --field="Select Your Timezone:":CB --field="Use UTC or Local Time?":CB --field="Choose a hostname:" --field="Choose a username:" --field="Enter Your User Password:H" --field="Re-enter Your User Password:H" --separator=" " \
"us!af!al!am!at!az!ba!bd!be!bg!br!bt!bw!by!ca!cd!ch!cm!cn!cz!de!dk!ee!es!et!eu!fi!fo!fr!gb!ge!gh!gn!gr!hr!hu!ie!il!in!iq!ir!is!it!jp!ke!kg!kh!kr!kz!la!lk!lt!lv!ma!md!me!mk!ml!mm!mn!mt!mv!ng!nl!no!np!pc!ph!pk!pl!pt!ro!rs!ru!se!si!sk!sn!sy!tg!th!tj!tm!tr!tw!tz!ua!uz!vn!za" "en_US.UTF-8 $locales" "$zones" "!UTC!Localtime" "" "" "" "" "yes!no" > config1.txt

sed -i 'N;s/\n/ /' config1.txt 
sed -i "s/  / /g" config1.txt

key=` cat config1.txt | awk '{print $1;}' `
locale=` cat config1.txt | awk '{print $2;}' `
zone=` cat config1.txt | awk '{print $3;}' `
clock=` cat config1.txt | awk '{print $4;}' `
hname=` cat config1.txt | awk '{print $5;}' `
username=` cat config1.txt | awk '{print $6;}' `
rtpasswd1=` cat config1.txt | awk '{print $7;}' `
rtpasswd2=` cat config1.txt | awk '{print $8;}' `

rm config1.txt

if [ "$rtpasswd1" != "$rtpasswd2" ]
        then zenity --error --title="$title" --text "The passwords did not match, please try again." --height=40
        config1
fi
}


setup() {
# generating locale
(echo "# Generating Locale..."
rm -f /etc/locale.conf
rm -f /etc/locale.gen
echo "LANG=\"${locale}\"" > /etc/locale.conf
echo "${locale} UTF-8" > /etc/locale.gen
locale-gen
export LANG=${locale}

#setting keymap
mkdir -p /etc/X11/xorg.conf.d/
rm -f /etc/X11/xorg.conf.d/00-keyboard.conf
echo -e 'Section "InputClass"\n	Identifier "system-keyboard"\n	MatchIsKeyboard "on"\n	Option "XkbLayout" "'$key'"\n	Option "XkbModel" "'$model'"\n	Option "XkbVariant" ",'$variant'"\n	 Option "XkbOptions" "grp:alt_shift_toggle"\nEndSection' > /etc/X11/xorg.conf.d/00-keyboard.conf

# setting timezone
echo "# Setting Timezone..."
rm /etc/localtime
ln -s /usr/share/zoneinfo/${zone}/${subzone} /etc/localtime

#setting hw clock
echo "# Setting System Clock..."
hwclock --systohc --$clock

#setting hostname
echo "# Setting Hostname..."
rm -f /etc/hostname
echo $hname > /etc/hostname
    
#root password
echo "# Setting root password..."
touch .passwd
echo -e "$rtpasswd1\n$rtpasswd2" > .passwd
passwd root < .passwd >/dev/null

# removing autostart files before new user is created
if [[ -f "/etc/skel/.config/openbox/autostart" ]];then
sed -i '/liveuser.sh/d' /etc/skel/.config/openbox/autostart
fi 
if [[ -f "/etc/skel/.config/i3/config" ]];then
sed -i '/liveuser.sh/d' /etc/skel/.config/i3/config
fi

# fixing root's bash_profile
sed -i '/startx/d' /root/bash_profile

#adding user
echo "# Making new user..."
userdel -rf liveuser
useradd -m -g users -G adm,lp,wheel,power,audio,video -s /bin/bash $username
passwd $username < .passwd >/dev/null
rm .passwd

# starting desktop manager
if [ "$desktop" = "Gnome" ]
    then systemctl enable gdm.service
else
    arch_chroot systemctl enable lightdm.service
    echo "theme-name = BlackMATE" >> /etc/lightdm/lightdm-gtk-greeter.conf
    echo "background = /usr/share/Wallpaper/Shadow_cast-RevengeOS-v2.png" >> /etc/lightdm/lightdm-gtk-greeter.conf
fi


echo "# Configuration Finished!" 
) | zenity --progress --title="$title" --width=450 --no-cancel

# removing files for oem install and configuration
rm -f /usr/bin/liveuser.sh
rm -f /root/.xinitrc
rm -f /root/.xsession
rm -rf /etc/systemd/system/getty@tty1.service.d
rm -f /etc/skel/.config/autostart/oem.desktop
rm -rf /etc/oem-install

# starting the DM
if [ "$desktop" = "Gnome" ]
    then systemctl enable gdm.service
         systemctl start gdm.service
else
    systemctl enable lightdm.service
    systemctl start lightdm.service
fi

}




# execution
config1
setup

