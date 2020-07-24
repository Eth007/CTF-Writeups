## Raymonds Recovery - 100 points - 133 solves

>Uh-oh! Someone corrupted all my important files and now I can’t open any of them. I really need one of them in particular, a png of something very important. Please help me recover it!
>
>Here, take this ext4 filesystem and see what you can find. If you can figure out which file it is and how to fix it, you’ll get something in return!

We open the file in Autopsy:

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/raymonds_recovery/1.PNG)

There seems to be nothing but corrupted JPEG files and pictures of hats. But then, we see the $CarvedFiles section:

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/raymonds_recovery/2.PNG)

We look through the files that Autopsy found, and we find a picture with the flag in it:

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/raymonds_recovery/3.PNG)

Flag: *uiuctf{everyb0dy_l0ves_raym0nd}*
