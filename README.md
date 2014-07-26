ua100mix
========

A try for a pyqt4 mixer for Roland/Edimax UA-100
================================================

Being neither a good programmer, nor a good musician (actually, not even an average on of them), 
I decided anyway to try write a pyQT4 mixer to control the old Roland UA-100.

There was a working mixer, written in C++ and MOTIF by Michael Minn (http://michaelminn.com/linux/mmusbaudio/), 
but it relies on OSS and thus it should not be working with ALSA. In fact, Michael's mixer *do* work with ALSA (with some workarounds like installing virtual midi devices in the kernel): nevertheless, the lack af a modern interface (MOTIF is *ancient*, isn't it?) makes it not so easy to manage.

I pretty like Qt (much better than gtk, my first love in the late '90s) so I'm trying pyQt - because python is easy enough for my poor programming skills.

If anyone is interested in helping, *YOU ARE WELCOME*! I'd appreciate even corrections or comments on my 
awful coding!

Wishmerhill
