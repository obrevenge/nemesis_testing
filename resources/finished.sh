#!/bin/bash
#
#  This file is part of Nemesis.
#
#  Nemesis is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Nemesis is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Nemesis; If not, see <http://www.gnu.org/licenses/>.

cd /home/liveuser/nemesis_testing/resources

source nemesis.conf

ans=$(zenity --list --radiolist --title="Nemesis Installer" --text "What would you like to do now?" --column "Select" --column "Option" FALSE Restart FALSE Close)

if [ "$ans" = "Restart" ]
	then reboot
	else
	killall get-nemesis.sh;exit
fi 
