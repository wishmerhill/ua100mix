# ua100mix
### A try for a pyqt4 mixer for Roland/Edirol UA-100


Being neither a good programmer, nor a good musician (actually, not even an average one on either of those tasks), 
I anyway decided to try writing a pyQt4 mixer to control the old Roland UA-100.

There used to be a working mixer, written in C++ and MOTIF by Michael Minn (http://michaelminn.com/linux/mmusbaudio/) back in the mid 2000s, but it relied on OSS and thus it should not work well with ALSA. In fact, Michael's mixer *do* work with ALSA (with some workarounds, like installing virtual midi devices in the kernel): nevertheless, the lack af a modern interface (MOTIF is *ancient*, isn't it?) makes it not so easy to manage.

I pretty like Qt (much better than gtk, even if it was my first love back in the late '90s) so I'm trying pyQt: python is easy enough for my poor programming skills and QtDesigner is a really good tool to create a nice interface.

If anyone is interested in helping me, *YOU ARE WELCOME*! I'd appreciate even corrections or comments on my 
awful coding!

## Install and use

### Prerequisites

In order to use the ua100mix you need **python** (2.7 is what I tested, no idea if older versions work). 
Besides, the ua100mix uses **mido** and **python-rtmidi**: the best way to install those libraries is with pip (https://pip.pypa.io/en/stable/).

I wrote the ua100mix on Gentoo Linux: I know it works on OpenSuse and Ubuntu. I have no idea if you can run it successfully on any other system.

### Install

To install ua100mix just clone the git repo to your computer. 

#### With git

```shell
$ mkdir devel
$ cd devel
$ git clone https://github.com/wishmerhill/ua100mix.git
```
#### Without git

If you don't have git and don't want to install one you can just open https://github.com/wishmerhill/ua100mix and click "Clone or download"-> "Download ZIP" in top-right corner of the page, then extract files wherever you like.

### Run ua100mix

From the ua100mix directory, launch main.py with your python interpreter:

```shell
$ cd ~/devel/ua100mix
$ python main.py
```

You can also create an executable for the program, so you don't have to use console all the time.
On Ubuntu, you can just create launcher from desktop via right-click menu (at least on 16.04 you can). You'll need to point out the path to extracted files (working directory) and enter a command python "main.py", then go to permissions tab and click "Allow this file to run as program".
You can do pretty much the same in any linux distributive by creating file with extension .sh in which you need to write pretty much the same you would do in terminal, then save it, open properties and again go to permissions tab and click "Allow this file to run as program".

## *portmidi* vs *mido + rtmidi*
The first version of the ua100mix used portmidi for sending MIDI messages to the UA-100. After a user told me about his problems with Ubuntu's funny and buggy portmidi version, I discovered how old and buggy portmidi itself is. So I moved the code to mido and rtmidi. I find it *way* better: thanks Semyon for your help!

###### A word about the "SaxMode" icon
I use this mixer mainly to record my exercises with the saxophone, so I need a quick way to set the input and output levels as well as the recording and playback sources.

![Just a sample screenshot...](/screenshots/ua-100_mix.png?raw=true "UA-100 Mixer at work")

Cheers,
Wishmerhill

Tags: Roland, Edirol, UA-100, UA 100, mixer, effects, pyhon, pyqt
