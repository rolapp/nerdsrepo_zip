# NersRepoZip

NerdsRepoZip ist ein kleines Hilfsprogramm, welches aus dem Addon-Ordner die passende Zip-Datei erstellt.
Das Programm ist in Python3 geschrieben. Als Zusatzmodul wird Tkinter benötigt.

## Windows

Im Ordner /src befindet sich der Python Quellcode für Windows
Die nerdsrepo_zip.exe führt das programm ohne Installation aus.
Die setup.exe installiet das Programm normal, so das es in der Programleiste aufgerufen werden kann und dem entsprechend auch deinstalliert werden.

## Linux

### debian

Im debian Ordner befindet sich ein Deb-Paket welches am besten in der Konsole mit apt-get install nerdsrepozip_1.0.1_all.deb installiert wird.
Alternativ kann auch gdebi verwendet werden, so ist gewährleistet das die Abhängkeiten (python3-tk) mit installiert werden.

### suse

Im suse Ordner befindet sich ein Rpm Paket welches die Abhänigkeit python3-tk mit installiert. Das paket ist gpg signiert. Der Publickey befindet sich zum import in public_key.txt
- rpm --import public_key.txt
- zypper install nerdsrepozip-1.0.1-1.suse.rpm
- oder über Yast installieren

### centos / fedora

Im centos Ordner befindet sich ein Rpm Paket welches die Abhänigkeit python-tkinter mit installiert. Das paket ist gpg signiert. Der Publickey befindet sich zum import in public_key.txt.
- rpm --import public-key.txt
- yum install nerdsrepozip-1.0.1-1.centos.rpm

Das Programm findet man bei den Linux Varianten unter Anwendungen -> Entwicklung

#### Das Program funktioniert unter dem Gnome3-Desktop teilweise nicht richtig, es kommt hier zu Fehlern in der Grafik.


