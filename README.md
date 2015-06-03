ua100mix
========

A try for a pyqt4 mixer for Roland/Edirol UA-100
================================================

Being neither a good programmer, nor a good musician (actually, not even an average one on both of them), 
I decided anyway to try writing a pyQT4 mixer to control the old Roland UA-100.

There was a working mixer, written in C++ and MOTIF by Michael Minn (http://michaelminn.com/linux/mmusbaudio/), 
but it relies on OSS and thus it should not be working with ALSA. In fact, Michael's mixer *do* work with ALSA (with some workarounds like installing virtual midi devices in the kernel): nevertheless, the lack af a modern interface (MOTIF is *ancient*, isn't it?) makes it not so easy to manage.

I pretty like Qt (much better than gtk, even if it was my first love back in the late '90s) so I'm trying pyQt - because python is easy enough for my poor programming skills.

If anyone is interested in helping, *YOU ARE WELCOME*! I'd appreciate even corrections or comments on my 
awful coding!

![Just a sample screenshot...](/screenshots/ua-100_mix.png?raw=true "UA-100 Mixer at work")


Wishmerhill

Tags: Roland, Edirol, UA-100, UA 100, mixer, effects, pyhon, pyqt
