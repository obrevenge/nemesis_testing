#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  nemesis.py
#
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
from xml.etree import ElementTree as ET 
import subprocess
import time

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Nemesis Installer")
        self.set_border_width(3)
        self.set_default_size(800, 500)
        """creating the notebook, main widget of the gui"""
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.LEFT)
        self.add(self.notebook)

        self.page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.p1box1 = Gtk.Box()
        self.p1box2 = Gtk.Box()
        self.p1box3 = Gtk.Box()
        self.p1box4 = Gtk.Box()
        self.p1box5 = Gtk.Box()
        self.page1.pack_start(self.p1box1, True, True, 0)
        self.page1.pack_start(self.p1box2, True, True, 0)
        self.page1.pack_start(self.p1box3, True, True, 0)
        self.page1.pack_start(self.p1box4, True, True, 0)
        self.page1.pack_start(self.p1box5, True, True, 0)
        self.p1label = Gtk.Label()
        self.p1label.set_markup("<big><b>Thank You for Choosing Revenge OS</b></big>")
        self.p1label2 = Gtk.Label("Click Next to Begin")
        self.p1label2.set_justify(Gtk.Justification.CENTER)
        self.p1box4.pack_start(self.p1label2, True, True, 0)

        """Front page image, the Revege OS image"""
        self.image = Gtk.Image()
        self.image = Gtk.Image.new_from_file('resources/revenge_logo_sm.png')
        self.p1box1.pack_start(self.p1label, True, True, 0)
        self.p1box3.pack_start(self.image, True, True, 0)

        self.p1buttonbox = Gtk.Box()

        self.p1next_button = Gtk.Button("Next")
        self.p1next_button.connect("clicked", self.next_page)
        self.p1buttonbox.pack_end(self.p1next_button, False, False, 0)

        # creating the list and store for the type button

        types = ["Normal", "OEM", "StationX"]

        type_store = Gtk.ListStore(str)

        # Adding the items to the list store to display in the combobox
        for type in types:
            type_store.append([type])

        self.typebutton = Gtk.ComboBox.new_with_model(type_store)
        renderer_text = Gtk.CellRendererText()
        self.typebutton.pack_start(renderer_text, True)
        self.typebutton.add_attribute(renderer_text, "text", 0)
        self.typebutton.set_active(0)
        self.typebutton.connect("changed", self.on_typebutton_changed)

        self.p1buttonbox.pack_start(self.typebutton, False, False, 0)


        self.page1.pack_start(self.p1buttonbox, False, False, 0)

        self.notebook.append_page(self.page1, Gtk.Label("Welcome"))


        # Page 2 Starts here


        self.page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.p2label = Gtk.Label()
        self.p2label.set_markup("<big><b>Partitoning</b></big>")
        # Creating the boxes for the second page layout
        self.p2box1 = Gtk.Box()
        self.p2box2 = Gtk.Box()
        self.p2box3 = Gtk.Box()
        self.p2box4 = Gtk.Box()
        self.p2box5 = Gtk.Box()
        self.p2box6 = Gtk.Box()
        self.p2box7 = Gtk.Box()
        self.p2box8 = Gtk.Box()
        self.p2box9 = Gtk.Box()

        self.p2box1.pack_start(self.p2label, True, True, 0)

        self.disk_label = Gtk.Label("Where do you want to install Revenge OS?")

        disks = subprocess.call('fdisk -l | grep Disk | grep -v label | grep -v identifier > disks.txt', shell=True)

        disk_store = Gtk.ListStore(str)

        with open('disks.txt', 'r') as f:
            disks_list = [line.strip() for line in f]

        for disk in disks_list:
            disk_store.append([disk])



        self.disk_button = Gtk.ComboBox.new_with_model(disk_store)
        renderer_text = Gtk.CellRendererText()
        self.disk_button.pack_start(renderer_text, True)
        self.disk_button.add_attribute(renderer_text, "text", 0)
        self.disk_button.set_active(0)
        self.disk_button.connect("changed", self.on_disk_button_changed)

        self.autopart_label = Gtk.Label()
        self.autopart_label.set_justify(Gtk.Justification.CENTER)
        self.autopart_label.set_markup("<big>Auto Partitioning</big>\nThis option will delete the selected drive and install Revenge OS")

        self.man_label = Gtk.Label()
        self.man_label.set_justify(Gtk.Justification.CENTER)
        self.man_label.set_markup("<big>Manual Partitioning</big>\nThis option will allow you to select exactly where to install Revenge OS")

        self.p2box2.pack_start(self.man_label, True, True, 0)

        self.p2box3.pack_start(self.autopart_label, True, True, 0)

        part_options = ["Automatic Partitioning", "Manual Partitioning"]

        part_store = Gtk.ListStore(str)

        for part in part_options:
            part_store.append([part])

        self.part_button = Gtk.ComboBox.new_with_model(part_store)
        renderer_text = Gtk.CellRendererText()
        self.part_button.pack_start(renderer_text, True)
        self.part_button.add_attribute(renderer_text, "text", 0)
        self.part_button.set_active(0)
        self.part_button.connect("changed", self.on_part_button_changed)

        self.p2box4.pack_start(self.part_button, True, False, 0)

        self.p2box6.pack_start(self.disk_label, True, False, 0)

        self.p2box5.pack_start(self.disk_button, True, False, 0)

        self.p2next_button = Gtk.Button("Next")
        self.p2next_button.connect("clicked", self.part_next_page)
        self.p2box7.pack_end(self.p2next_button, False, False, 0)

        self.btloader_button = Gtk.CheckButton.new_with_label("Install Bootloader")
        self.btloader_button.set_active(True)
        self.btloader_button.connect("toggled", self.on_btloader_button_toggled)

        self.p2box7.pack_start(self.btloader_button, False, False, 0)

        self.page2.pack_start(self.p2box1, True, True, 0)
        self.page2.pack_start(self.p2box2, True, True, 0)
        self.page2.pack_start(self.p2box3, True, True, 0)
        self.page2.pack_start(self.p2box4, False, False, 0)
        self.page2.pack_start(self.p2box8, True, True, 0)
        self.page2.pack_start(self.p2box6, False, False, 0)
        self.page2.pack_start(self.p2box5, False, False, 0)
        self.page2.pack_start(self.p2box9, True, True, 0)
        self.page2.pack_start(self.p2box7, False, False, 0)

        self.notebook.append_page(self.page2, Gtk.Label("Partitioning"))


        # Page 3 Starts here

        self.page3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.p3label = Gtk.Label()
        self.p3label.set_markup("<big><b>Timezone Language and Keyboard</b></big>")


        self.p3box1 = Gtk.Box()
        self.p3box2 = Gtk.Box()
        self.p3box3 = Gtk.Box()
        self.p3box4 = Gtk.Box()
        self.p3box5 = Gtk.Box()
        self.p3box6 = Gtk.Box()
        self.p3box7 = Gtk.Box()
        self.p3box8 = Gtk.Box()
        self.p3box9 = Gtk.Box()

        self.tz_label = Gtk.Label()
        self.tz_label.set_justify(Gtk.Justification.CENTER)
        self.tz_label.set_markup("Select Your Timezone")

        self.lg_label = Gtk.Label()
        self.lg_label.set_justify(Gtk.Justification.CENTER)
        self.lg_label.set_markup("Select Your Language")

        self.key_label = Gtk.Label()
        self.key_label.set_justify(Gtk.Justification.CENTER)
        self.key_label.set_markup("Select Your Keyboard")

        self.p3box1.pack_start(self.p3label, True, True, 0)

        self.p3box2.pack_start(self.tz_label, True, True, 0)

        self.p3box4.pack_start(self.lg_label, True, True, 0)

        self.p3box6.pack_start(self.key_label, True, True, 0)


        tree = ET.parse("resources/locales.xml")
        var1 = tree.findall(".//language_name")
        tz_name_list = [t.text for t in var1]

        tz_store = Gtk.ListStore(str)

        for tz in tz_name_list:
            tz_store.append([tz])

        self.tz_button = Gtk.ComboBox.new_with_model(tz_store)
        renderer_text = Gtk.CellRendererText()
        self.tz_button.pack_start(renderer_text, True)
        self.tz_button.add_attribute(renderer_text, "text", 0)
        self.tz_button.set_active(0)
        self.tz_button.connect("changed", self.on_tz_button_changed)

        tree = ET.parse("resources/timezones.xml")
        var4 = tree.findall(".//timezone_name")
        timezone_name_list = [t.text for t in var4]

        timezone_store = Gtk.ListStore(str)

        for tz in timezone_name_list:
            timezone_store.append([tz])



        self.timezone_button = Gtk.ComboBox.new_with_model(timezone_store)
        renderer_text = Gtk.CellRendererText()
        self.timezone_button.pack_start(renderer_text, True)
        self.timezone_button.add_attribute(renderer_text, "text", 0)
        self.timezone_button.set_active(0)
        self.timezone_button.connect("changed", self.on_timezone_button_changed)







        self.page3.pack_start(self.p3box1, True, True, 0)
        self.page3.pack_start(self.p3box2, True, True, 0)
        self.page3.pack_start(self.p3box3, False, False, 0)
        self.page3.pack_start(self.p3box4, True, True, 0)
        self.page3.pack_start(self.p3box5, False, False, 0)
        self.page3.pack_start(self.p3box6, True, True, 0)
        self.page3.pack_start(self.p3box7, False, False, 0)
        self.page3.pack_start(self.p3box9, True, True, 0)
        self.page3.pack_start(self.p3box8, False, False, 0)

        self.p3box5.pack_start(self.tz_button, True, False, 0)

        self.p3box3.pack_start(self.timezone_button, True, False, 0)

        keys = ['us', 'af', 'al', 'am', 'at', 'az', 'ba', 'bd', 'be', 'bg', 'br', 'bt', 'bw', 'by', 'ca', 'cd', 'ch', 'cm', 'cn', 'cz', 'de', 'dk', 'ee', 'es', 'et', 'eu', 'fi', 'fo', 'fr', 'gb', 'ge', 'gh', 'gn', 'gr', 'hr', 'hu', 'ie', 'il', 'in', 'iq', 'ir', 'is', 'it', 'jp', 'ke', 'kg', 'kh', 'kr', 'kz', 'la', 'lk', 'lt', 'lv', 'ma', 'md', 'me', 'mk', 'ml', 'mm', 'mn', 'mt', 'mv', 'ng', 'nl', 'no', 'np', 'pc', 'ph', 'pk', 'pl', 'pt', 'ro', 'rs', 'ru', 'se', 'si', 'sk', 'sn', 'sy', 'tg', 'th', 'tj', 'tm', 'tr', 'tw', 'tz', 'ua', 'uz', 'vn', 'za']

        keyboard_store = Gtk.ListStore(str)

        for key in keys:
            keyboard_store.append([key])


        self.keyboard_button = Gtk.ComboBox.new_with_model(keyboard_store)
        renderer_text = Gtk.CellRendererText()
        self.keyboard_button.pack_start(renderer_text, True)
        self.keyboard_button.add_attribute(renderer_text, "text", 0)
        self.keyboard_button.set_active(0)
        self.keyboard_button.connect("changed", self.on_keyboard_button_changed)

        self.p3box7.pack_start(self.keyboard_button, True, False, 0)

        self.p3next_button = Gtk.Button("Next")
        self.p3next_button.connect("clicked", self.loc_next_page)
        self.p3box8.pack_end(self.p3next_button, False, False, 0)




        self.notebook.append_page(self.page3, Gtk.Label("Location"))


        # Page 4 starts here

        self.page4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.p4label = Gtk.Label()
        self.p4label.set_markup("<big><b>Desktop</b></big>")

        self.p4box1 = Gtk.Box()
        self.p4box2 = Gtk.Box()
        self.p4box3 = Gtk.Box()
        self.p4box4 = Gtk.Box()
        self.p4box5 = Gtk.Box()

        self.p4box1.pack_start(self.p4label, True, True, 0)

        self.page4.pack_start(self.p4box1, True, True, 0)
        self.page4.pack_start(self.p4box2, True, True, 0)
        self.page4.pack_start(self.p4box3, False, False, 0)
        self.page4.pack_start(self.p4box4, True, True, 0)
        self.page4.pack_start(self.p4box5, False, False, 0)

        desktops_list = ['OBR Openbox', 'XFCE', 'Mate', 'Gnome', 'KDE PLasma', 'i3']

        desktop_store = Gtk.ListStore(str)

        for desktop in desktops_list:
            desktop_store.append([desktop])

        self.desktop_button = Gtk.ComboBox.new_with_model(desktop_store)
        renderer_text = Gtk.CellRendererText()
        self.desktop_button.pack_start(renderer_text, True)
        self.desktop_button.add_attribute(renderer_text, "text", 0)
        self.desktop_button.set_active(0)
        self.desktop_button.connect("changed", self.on_desktop_button_changed)

        self.p4box3.pack_start(self.desktop_button, True, False, 0)

        self.p4next_button = Gtk.Button("Next")
        self.p4next_button.connect("clicked", self.desktop_next_page)
        self.p4box5.pack_end(self.p4next_button, False, False, 0)

        self.desktop_image = Gtk.Image()
        self.desktop_image = Gtk.Image.new_from_file('resources/desktops.png')

        self.p4box2.pack_start(self.desktop_image, True, True, 0)


        self.notebook.append_page(self.page4, Gtk.Label("Dekstop"))


        # starting page 5

        self.page5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.p5box1 = Gtk.Box()
        self.p5box2 = Gtk.Box()
        self.p5box3 = Gtk.Box()
        self.p5box4 = Gtk.Box()
        self.p5box5 = Gtk.Box()
        self.p5box6 = Gtk.Box()

        self.p5label = Gtk.Label()
        self.p5label.set_markup("<big><b>New User</b></big>")

        self.p5box1.pack_start(self.p5label, True, True, 0)



        self.page5.pack_start(self.p5box1, True, False, 0)
        self.page5.pack_start(self.p5box2, True, False, 0)
        self.page5.pack_start(self.p5box3, True, False, 0)
        self.page5.pack_start(self.p5box4, True, False, 0)
        self.page5.pack_start(self.p5box5, True, False, 0)
        self.page5.pack_start(self.p5box6, False, False, 0)


        

        self.hname_label = Gtk.Label("Name Your Computer:")
        self.username_label = Gtk.Label("Enter Your Username:")
        self.password1_label = Gtk.Label("Enter Your Password:")
        self.password2_label = Gtk.Label("Re-enter Your Password:")

        self.hname_entry = Gtk.Entry()
        self.hname_entry.set_text("revengeos")
        self.username_entry = Gtk.Entry()
        self.password1_entry = Gtk.Entry()
        self.password1_entry.set_visibility(False)
        self.password2_entry = Gtk.Entry()
        self.password2_entry.set_visibility(False)

        self.p5box2.pack_start(self.hname_label, False, False, 0)
        self.p5box3.pack_start(self.username_label, False, False, 0)
        self.p5box4.pack_start(self.password1_label, False, False, 0)
        self.p5box5.pack_start(self.password2_label, False, False, 0)

        self.p5box2.pack_end(self.hname_entry, False, False, 0)
        self.p5box3.pack_end(self.username_entry, False, False, 0)
        self.p5box4.pack_end(self.password1_entry, False, False, 0)
        self.p5box5.pack_end(self.password2_entry, False, False, 0)

        self.p5next_button = Gtk.Button("Next")
        self.p5next_button.connect("clicked", self.user_next_page)
        self.p5box6.pack_end(self.p5next_button, False, False, 0)

        self.notebook.append_page(self.page5, Gtk.Label("New User"))


        # starting page 6

        self.page6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.confirm_label = Gtk.Label()
        self.confirm_label.set_markup("<big><b>Confirm</b></big>")

        self.p6box1 = Gtk.Box()
        self.p6box2 = Gtk.Box()
        self.p6box3 = Gtk.Box()

        confirm_text = "Are you ready to start the installation?\n\nClick 'Next' to continue or 'Cancel' to cancel the installation."

        self.p6box1.pack_start(self.confirm_label, True, True, 0)

        self.confirm_item_label = Gtk.Label(confirm_text)

        self.p6next_button = Gtk.Button("Next")
        self.p6next_button.connect("clicked", self.on_p6next_button_clicked)

        self.cancel_button = Gtk.Button("Cancel")
        self.cancel_button.connect("clicked", self.on_cancel_button_clicked)

        self.p6box2.pack_start(self.confirm_item_label, True, True, 0)

        self.p6box3.pack_start(self.cancel_button, False, False, 0)
        self.p6box3.pack_end(self.p6next_button, False, False, 0)


        self.page6.pack_start(self.p6box1, False, False, 0)
        self.page6.pack_start(self.p6box2, True, True, 0)
        self.page6.pack_end(self.p6box3, False, False, 0)





        self.notebook.append_page(self.page6, Gtk.Label("Confirm"))

        # beginning page 7, last page (I hope!!!)

        self.page7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)


        self.p7box1 = Gtk.Box()
        self.p7box2 = Gtk.Box()
        self.p7box3 = Gtk.Box()

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(0.0)

        self.p7box2.pack_start(self.progressbar, True, True, 0)

        self.install_label = Gtk.Label("Installing...\nThank you for Choosing Revenge OS!\n\nInstallation will be finished in a few minutes.")

        self.p7box1.pack_start(self.install_label, True, True, 0)

        self.page7.pack_start(self.p7box1, True, True, 0)
        self.page7.pack_start(self.p7box2, False, True, 0)
        self.page7.pack_start(self.p7box3, True, True, 0)

        self.notebook.append_page(self.page7, Gtk.Label("Intalling"))


    def on_p6next_button_clicked(self, widget):
        self.notebook.next_page()

        self.progressbar.set_text("Starting")
        self.progressbar.set_show_text("some_text")
        self.progressbar.set_fraction(0.1)
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(2)

        self.progressbar.set_text("Continuing")
        self.progressbar.set_show_text("some_text")
        self.progressbar.set_fraction(0.3)
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(2)

        self.progressbar.set_text("Halfway")
        self.progressbar.set_show_text("some_text")
        self.progressbar.set_fraction(0.5)
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(2)

        self.progressbar.set_text("Three Quarters")
        self.progressbar.set_show_text("some_text")
        self.progressbar.set_fraction(0.8)
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(2)

        self.progressbar.set_text("Finished")
        self.progressbar.set_show_text("some_text")
        self.progressbar.set_fraction(1.0)
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(2)


    def on_cancel_button_clicked(self, widget):
        Gtk.main_quit()



    def user_next_page(self, widget):
        hname = self.hname_entry.get_text()
        username = self.username_entry.get_text()
        password1 = self.password1_entry.get_text()
        password2 = self.password2_entry.get_text()

        print(hname, username, password1, password2)

        if password1 != password2:
            subprocess.call('./scripts/password-error.sh')

        if hname.islower() != True:
            subprocess.call('./scripts/hname-error.sh')

        if username.islower() != True:
            subprocess.call('./scripts/username-error.sh')

        self.notebook.next_page()

        f = open("resources/nemesis.conf", "a")
        f.write( "hname='" + hname + "'\n")
        f.write( "username='" + username + "'\n")
        f.write( "rtpasswd1='" + password1 + "'\n")
        f.write( "rtpasswd2='" + password2 + "'\n")

        f.close()



    def desktop_next_page(self, widget):
        tree_iter = self.desktop_button.get_active_iter()
        if tree_iter != None:
            model = self.desktop_button.get_model()
            desktop = model[tree_iter][0]
            print(desktop)

        f = open("resources/nemesis.conf", "a")
        f.write( "desktop='" + desktop + "'\n")

        f.close()

        self.notebook.next_page()



    def on_desktop_button_changed(self, widget):
        tree_iter = self.desktop_button.get_active_iter()
        if tree_iter != None:
            model = self.desktop_button.get_model()
            desktop = model[tree_iter][0]
            print(desktop)

    def on_btloader_button_toggled(self, widget):
        btloader = self.btloader_button.get_active()
        print(btloader)


    def on_disk_button_changed(self, widget):
        tree_iter = self.disk_button.get_active_iter()
        if tree_iter != None:
            model = self.disk_button.get_model()
            disk = model[tree_iter][0]
            print(disk)

    def loc_next_page(self, widget):
        tree_iter = self.tz_button.get_active_iter()
        if tree_iter != None:
            model = self.tz_button.get_model()
            tz = model[tree_iter][0]
            print(tz)
            tree = ET.parse("resources/locales.xml")
            var2 = tree.findall(".//locale_name")
            locale_list = [t.text for t in var2]
            tree = ET.parse("resources/locales.xml")
            var1 = tree.findall(".//language_name")
            tz_name_list = [t.text for t in var1]
            tz2 = tz_name_list.index('{}'.format(tz))
            code1 = int(tz2)
            locale = locale_list[code1].format(code1 = code1)
            print(locale)

        tree_iter = self.timezone_button.get_active_iter()
        if tree_iter != None:
            model = self.timezone_button.get_model()
            timezone = model[tree_iter][0]
            print(timezone)

        tree_iter = self.keyboard_button.get_active_iter()
        if tree_iter != None:
            model = self.keyboard_button.get_model()
            keyboard = model[tree_iter][0]
            print(keyboard)

        f = open("resources/nemesis.conf", "a")
        f.write( "locale='" + locale + "'\n")
        f.write( "key='" + keyboard + "'\n")
        f.write( "timezone='" + timezone + "'\n")

        f.close()

        self.notebook.next_page()


    def on_keyboard_button_changed(self, widget):
        tree_iter = self.keyboard_button.get_active_iter()
        if tree_iter != None:
            model = self.keyboard_button.get_model()
            keyboard = model[tree_iter][0]
            print(keyboard)


    def on_timezone_button_changed(self, widget):
        tree_iter = self.timezone_button.get_active_iter()
        if tree_iter != None:
            model = self.timezone_button.get_model()
            timezone = model[tree_iter][0]
            print(timezone)



    def on_tz_button_changed(self, widget):
        tree_iter = self.tz_button.get_active_iter()
        if tree_iter != None:
            model = self.tz_button.get_model()
            tz = model[tree_iter][0]
            print(tz)
            tree = ET.parse("resources/locales.xml")
            var2 = tree.findall(".//locale_name")
            locale_list = [t.text for t in var2]
            tree = ET.parse("resources/locales.xml")
            var1 = tree.findall(".//language_name")
            tz_name_list = [t.text for t in var1]
            tz2 = tz_name_list.index('{}'.format(tz))
            code1 = int(tz2)
            locale = locale_list[code1].format(code1 = code1)
            print(locale)



    def on_part_button_changed(self, widget):
        tree_iter = self.part_button.get_active_iter()
        if tree_iter != None:
            model = self.part_button.get_model()
            part = model[tree_iter][0]
            print(part)


    def on_typebutton_changed(self, widget):
        tree_iter = self.typebutton.get_active_iter()
        if tree_iter != None:
            model = self.typebutton.get_model()
            install_type = model[tree_iter][0]
            print(install_type)

    def part_next_page(self, widget):
        tree_iter = self.part_button.get_active_iter()
        if tree_iter != None:
            model = self.part_button.get_model()
            part = model[tree_iter][0]

        if part == 'Manual Partitioning':
            subprocess.call('gparted', shell=True)
            subprocess.call('resources/man_part.sh', shell=True)

        self.notebook.next_page()
        print(part)

        f = open("resources/nemesis.conf", "a")
        f.write( "part='" + part + "'\n")

        f.close()


        tree_iter = self.disk_button.get_active_iter()
        if tree_iter != None:
            model = self.disk_button.get_model()
            disk = model[tree_iter][0]
            print(disk)

        btloader = self.btloader_button.get_active()
        print(btloader)

        if btloader == True:
            bootloader = 'Yes'
        else:
            bootloader = 'No'

        f = open("resources/nemesis.conf", "a")
        f.write( "grub='" + bootloader + "'\n")

        f.close()

    def next_page(self, widget):
        tree_iter = self.typebutton.get_active_iter()
        if tree_iter != None:
            model = self.typebutton.get_model()
            install_type = model[tree_iter][0]

        self.notebook.next_page()
        print(install_type)

        f = open("resources/nemesis.conf", "w")
        f.write( "type='" + install_type + "'\n")

        f.close()










win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()