#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nerds-upload.py

## imports
import tkinter as tk
import os, zipfile, sys
import webbrowser
import tempfile
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from xml.dom import minidom
from configparser import ConfigParser

config = ConfigParser()
_home = str(os.path.expanduser('~'))
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
img_dir = os.path.join(base_path, 'img')
config_file = os.path.join(_home + '/.config/nerdsrepo_config.ini')

## make default config.ini
if not os.path.isfile(config_file):

	config.set('DEFAULT', 'AddonDir', _home)
	config.set('DEFAULT', 'ZipDir', _home)
	config.add_section('REPO')
	config.set('REPO', 'RepoUrl', "https://repo.kodinerds.net/repo?action=login" )
	with open(config_file, 'w') as f:
		config.write(f)

## read config.ini
config.read(config_file)
AddonDir = config.get('DEFAULT','AddonDir')
ZipDir = config.get('DEFAULT','ZipDir')
URL = config.get('REPO','RepoUrl')

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):

    def __init__(self,**kwargs):
        tk.Tk.__init__(self,**kwargs)
        self.zipname = StringVar()
        ### Images ###
        self.img_win = PhotoImage(file = img_dir + '/icon.png')
        # main Window
        self.geometry('420x330+440+352')
        self.minsize(420,330)
        self.title("Nerdsrepo Zipfile ")
        self.configure(background='#CECECE')
        self.maxsize(504,396)
        self.iconphoto(False, self.img_win)

        self.option_add('*Dialog.msg.font', 'Helvetica 12 italic')
        self.option_add('*Dialog.msg.width', '600px')
        self.option_add("*Dialog.msg.wrapLength", 600)

        # Menubar
        self.menu = Menu(self)
        self.menu.pack()
        # Frame_1
        self.frame_1 = Frame_1(self)
        self.frame_1.place(relwidth= 0.9, relheight=0.50, relx=0.05, rely=0.05)
        # CraeteZip
        self.czip = CreateZip(self)
        self.czip.place(relwidth= 0.9, relheight=0.30, relx=0.05, rely=0.58)
        # Statusbar
        self.label_status = tk.Label(self, bd=1, relief='sunken', bg = '#D4D4D4')
        self.label_status.place(relwidth= 0.9, relheight=0.07, relx=0.05, rely=0.9)


    #### Funktionen
    def set_status(self, label='', status=''):
        if status == 'ERROR':
            bg = '#FF0000'
            fg = '#FFF'
        elif status == 'OK':
            bg = '#90EE90'
            fg = '#000'
        else:
            bg = '#D4D4D4'
            fg = '#000'
        self.label_status.config(text=label, bg=bg, fg=fg)

#    def write_config(self, key, value):

    def addon_dir(self):
        name = filedialog.askdirectory(initialdir=os.path.dirname(addondir.get()))
        if not name: return
        addondir.set(name)
        ret = self.is_addon(addondir.get())
        if ret == False: return False
        if CheckVar1 == 1:
            zipdir.set(name)

    def zip_dir(self):
        name = filedialog.askdirectory(initialdir=zipdir.get())
        zipdir.set(name)
        self.set_status()

    def set_zip(self):
        addon_dir = addondir.get()
        zip_dir = zipdir.get()
        create_zip(addon_dir,zip_dir)

    def is_addon(self, addon_dir):
        if not os.path.isdir(addon_dir):
            self.set_status("Verzeichnis existiert nicht!", 'ERROR')
            return False
        fname = os.path.join(addondir.get() + '/addon.xml')
        if not os.path.isfile(fname):
            self.set_status("Das verzeichnis scheint kein Kodi Addon zu sein!", 'ERROR')
            return False
        addondir.set(os.path.normpath(addondir.get()))
        self.set_status('Addon: ' + os.path.basename(addondir.get()),'OK')
        return fname

    def parse_xml(self, fname, matrix):
        xmldoc = minidom.parse(os.path.join(fname))
        itemlist = xmldoc.getElementsByTagName('addon')
        a_id = itemlist[0].attributes['id'].value
        a_version = itemlist[0].attributes['version'].value
        if matrix == 'matrix':
            sp=re.split('.*[0-9]', a_version)
            if sp[1]:
                self.set_status(a_version + ' Prefix schon vorhanden!', 'ERROR')
                return False
        _zipname_ = a_id + '-' +  a_version
        return _zipname_

    def edit_xml(self, fname):
        tempdir = tempfile.mkdtemp()
        tempname = os.path.join(tempdir, 'addon.xml')
        xmldoc = minidom.parse(fname)

        itemlist = xmldoc.getElementsByTagName('addon')
        a_version = itemlist[0].getAttribute('version')

        itemlist[0].setAttribute('version', a_version+'+matrix')
        reqlist = xmldoc.getElementsByTagName('import')
        for i in range(len(reqlist)):
            if reqlist[i].getAttribute('addon') == 'xbmc.python':
                reqlist[i].setAttribute('version', '3.0.0')
        with open(tempname, "w") as f:
            xmldoc.writexml(f)
        # modify header
        with open(tempname, 'r') as f:
            lines = f.readlines()
        old = '<?xml version="1.0" ?>'
        new = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
        lines[0] = lines[0].replace(old, new)
        with open(tempname, 'w') as fout:
            fout.write(''.join(lines))

        return tempname

    def make_archive(self, directory, zipname, matrix=''):
        fname=''
        if os.path.exists(directory):
            try:
                outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
            except Exception as e:
                self.set_status(str(e), 'ERROR')
                return
            # The root directory within the ZIP file.
            rootdir = os.path.basename(directory)

            for dirpath, dirnames, filenames in os.walk(directory):
                for dirname in dirnames:
                    for elem in ['.git', '__pycache__']:
                        if elem in dirname: dirnames.remove(dirname)
                for filename in filenames:
                    for elem in ['.zip', '.pyo']:
                        if elem in filename: filenames.remove(filename)
                for filename in filenames:
                    # Write the file named filename to the archive,
                    # giving it the archive name 'arcname'.
                    filepath = os.path.join(dirpath, filename)
                    parentpath = os.path.relpath(filepath, directory)
                    arcname    = os.path.join(rootdir, parentpath)
                    if matrix == 'matrix':
                        if filename == 'addon.xml':
                            fname = (self.edit_xml(filepath))
                            filepath = os.path.join(dirpath, fname)
                    outZipFile.write(filepath, arcname)
            outZipFile.close()
        if os.path.exists(fname):
            os.remove(fname)
            os.removedirs((os.path.dirname(fname)))

    def create_zip(self, postfix='.zip', matrix=''):
        ret = self.is_addon(addondir.get())
        if ret == False: return
        zipname = self.parse_xml(ret, matrix)
        if zipname == False: return
        out = zipdir.get() + '/' + zipname + postfix
        self.make_archive(addondir.get(), out, matrix)
        fname = os.path.join(out)
        if os.path.exists(fname):
            self.set_status(zipname + postfix + " wurde erstellt!", 'OK')
        return fname

    def open_browser(self):
        webbrowser.open(URL, new=2)

    def make_matrix(self):
        ret = self.create_zip('+matrix.zip', 'matrix')

    def write_config(self, part, key, value):

        result = messagebox.askokcancel('Default ' + key,
                                        value + '\nals Default Verzeichnis fest legen?',
                                        icon='question',
                                        default = 'cancel'
                                       )
        if result == True:
            config.set(part, key, value)
            with open(config_file, 'w') as f:
                config.write(f)

class Menu(tk.Frame):

    def __init__(self,master, **kwargs):
        tk.Frame.__init__(self,master,**kwargs)
        self.master = master
        self.img_quit = PhotoImage(file = img_dir + '/application-exit.png')
        self.img_help = PhotoImage(file = img_dir + '/help.png')
        self.img_info = PhotoImage(file = img_dir + '/about.png')
        # widget definitions
        self.menubar = tk.Menu(self, relief='flat', tearoff=0, bg='#D4D4D4')
        self.menubar.add_command(label="Beenden", image = self.img_quit, compound='left', command=master.quit)
        self.menubar.add_command(label="Hilfe", image = self.img_help, compound='left', command=self.Help)
        self.menubar.add_command(label="Info", image = self.img_info, compound='left', command=self.Info)
        master.config(menu=self.menubar)

    def Help(self):
        messagebox.showinfo('Hilfe', '- Die Anwendung ist selbst erklärend.\n\
- mit Rechtsklick auf das Eingabefeld kann der Pfad als Vorgabe gespeichert werden.\n\
- Die Funktion "Zip für Matrix erstellen" ändert an der addon.xml folgendes:\n\
      * <import addon="xbmc.python" version="3.0.0"/>\n\
      * der addon version wird +matrix angehängt.\n\
- Der Web-Browser-Button öffnet Das KodiNerdsRepo mit dem Standard-Browser', icon='question')

    def Info(self):
       messagebox.showinfo('über Nerdsrepo Zipfile', 'Version: 1.0.1\n\
\nDie Anwendung erstellt aus dem Addon-Verzeichnis eine Zip-Datei.\n\
Die Zipdatei entspricht den Kodi-Richtlinien (Addon_Id + Version) \n\
\n\n\t Copyright (c) 2020 Steffen Rolapp\n\n')



class Frame_1(tk.Frame):

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self,master,**kwargs)
        self.master = master

        global addondir
        global zipdir
        global CheckVar1

        self.CheckVar1  = IntVar()
        # widget definitions
        self.frame_1 = tk.Frame(self, relief='sunken', bd=1, bg='#D4D4D4')
        self.frame_1.place(relwidth= 1, relheight=1)

        # Addon Verzeichnis auwählen
        self.label_1 = tk.Label(self.frame_1, pady=5, text='Addon Verzeichnis auswählen', bg='#D4D4D4')
        self.label_1.place(relx=0.02, rely=0.02)
        addondir = tk.StringVar(self,AddonDir)
        self.dir_a = tk.Entry(self.frame_1, bd=1, bg='#FFF', textvariable=addondir)
        self.dir_a.place(relx=0.23, rely=0.2, relwidth='0.75')
        self.dir_button = tk.Button(self.frame_1, text='Suchen', command=self.master.addon_dir, width=5, activebackground="#ADD8E6" ,bg='#CECECE')
        self.dir_button.place(relx=0.02, rely=0.18)
        self.dir_a.bind('<ButtonPress-3>', self.make_dir_permanent)
        self.dir_a.bind('<FocusOut>', self.a_dir_fokusout)
        self.dir_a.bind('<ButtonPress-1>', self.a_dir_fokusin)
        self.dir_a.bind('<KeyPress>', self.a_dir_key)

        # Zip Verzeichnis auswählen
        self.label_2 = tk.Label(self.frame_1, text='Zip Datei Speichern unter', bg='#D4D4D4')
        self.label_2.place(rely=0.39, relx=0.02)
        zipdir = tk.StringVar(self,ZipDir)
        self.dir_z = tk.Entry(self.frame_1, bd=1, bg='#FFF', textvariable=zipdir)
        self.dir_z.place(relx=0.23, rely=0.55,  relwidth='0.75')
        self.zip_button = tk.Button(self.frame_1, text='Suchen', width=5, command=self.master.zip_dir, activebackground="#ADD8E6", bg='#CECECE')
        self.zip_button.place(relx=0.02, rely=0.53)
        self.dir_z.bind('<ButtonPress-3>', self.make_dir_permanent)

        # ZipDir = AddonDir
        CheckVar1 = IntVar()
        self.zip_is_add = tk.Checkbutton(self.frame_1,text = 'Zip-Datei im Addonverzeichnis speichern',bd=0, bg='#D4D4D4', variable = self.CheckVar1,  onvalue = 1, offvalue = 0, command=self.naccheck, activebackground="#ADD8E6")
        self.zip_is_add.pack(side = BOTTOM, anchor = W, padx = 5, pady =12)

    def naccheck(self):
        if self.CheckVar1 == 1:
            self.dir_z.configure(state='disabled')
            self.zip_button.configure(state='disable')
            self.CheckVar1 = 0
            zipdir.set(addondir.get())
        else:
            self.dir_z.configure(state='normal')
            self.zip_button.configure(state='normal')
            self.CheckVar1 = 1

    def make_dir_permanent(self, event):
        if event.widget == self.dir_a:
            self.master.write_config('DEFAULT', 'AddonDir', addondir.get())
        if event.widget == self.dir_z:
            self.master.write_config('DEFAULT', 'ZipDir', zipdir.get())

    def a_dir_fokusout(self,event):
        if event.widget == self.dir_a:
            print(addondir.get())
            self.master.is_addon(addondir.get())

    def a_dir_fokusin(self,event):
        if event.widget == self.dir_a:
            self.master.set_status()

    def a_dir_key(self, event):
        if event.widget == self.dir_a:
            if event.char =='\r':
                self.master.is_addon(addondir.get())

class CreateZip(tk.Frame):

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self,master,**kwargs)
        self.master = master
        global zipname
        zipname = tk.StringVar(self)
        self.img_web = PhotoImage(file = img_dir + '/web.png')
        self.img_save = PhotoImage(file = img_dir + '/document-save.png')
        self.czip = tk.Frame(self, relief='sunken', bd=1,bg='#D4D4D4')
        self.czip.place(relwidth= 1, relheight=1)
        # Zip erstellen
        self.label_3 = tk.Label(self, text='Zip Datei erstellen',bg='#D4D4D4')
        self.label_3.place(rely=0.17, relx=0.32)
        self.save_button1 = tk.Button(self, text='erstellen', bg='#CECECE', image=self.img_save, width=76, command=self.master.create_zip, activebackground="#90EE90", compound="left")
        self.save_button1.place(rely=0.10, relx=0.02)

        # Make Matrix Addon
        self.label_3 = tk.Label(self, text='Zip für Matrix erstellen',bg='#D4D4D4')
        self.label_3.place(rely=0.53, relx=0.32)
        self.label_4 = tk.Label(self, text='inkl. Anpassung der addon.xml', fg='#A52A2A',bg='#D4D4D4', font=('times', '10', 'italic'))
        self.label_4.place(relx=0.32, rely=0.71)
        self.save_button2 = tk.Button(self, text='erstellen',bg='#CECECE', image=self.img_save, width=76, command=self.master.make_matrix, activebackground="#90EE90", compound="left")
        self.save_button2.place(rely=0.54, relx=0.02)

        # Go to Web
        self.web_button = tk.Button(self,bg='#CECECE', image=self.img_web, width=60, height=60, command=self.master.open_browser, activebackground="#90EE90")
        self.web_button.pack(anchor='e', padx=10, pady=10)

#--------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
