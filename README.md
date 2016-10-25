ua100mix
========

A try for a pyqt4 mixer for Roland/Edirol UA-100
================================================

Being neither a good programmer, nor a good musician (actually, not even an average one on either of those tasks), 
I anyway decided to try writing a pyQt4 mixer to control the old Roland UA-100.

There used to be a working mixer, written in C++ and MOTIF by Michael Minn (http://michaelminn.com/linux/mmusbaudio/) back in the mid 2000s, but it relied on OSS and thus it should not work well with ALSA. In fact, Michael's mixer *do* work with ALSA (with some workarounds, like installing virtual midi devices in the kernel): nevertheless, the lack af a modern interface (MOTIF is *ancient*, isn't it?) makes it not so easy to manage.

I pretty like Qt (much better than gtk, even if it was my first love back in the late '90s) so I'm trying pyQt: python is easy enough for my poor programming skills and QtDesigner is a really good tool to create a nice interface.

If anyone is interested in helping me, *YOU ARE WELCOME*! I'd appreciate even corrections or comments on my 
awful coding!

A word about the "SaxMode" icon
===============================
I use this mixer mainly to record my excercizes with the saxophone, so I need a quick way to set the input and output levels as well as the recording and playback sources.

![Just a sample screenshot...](/screenshots/ua-100_mix.png?raw=true "UA-100 Mixer at work")

Cheers,
Wishmerhill

Tags: Roland, Edirol, UA-100, UA 100, mixer, effects, pyhon, pyqt
