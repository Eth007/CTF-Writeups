## Kernel::Time_To_Start - 100 points - 91 solves

>Welcome to pwnyOS!!
>
>pwnyOS is a custom x86 operating system that supports link-time kASLR, multitasking and kernel threads, execution of genuine ELF files, a realtime high resolution graphics engine, and a custom hierarchical file system. This OS was written from the ground up with its use as a challenge for UIUCTF 2020 in mind. All source code in the OS is 100% custom handwritten C and assembly- there are no libraries used, and none of its code can be found anywhere online. This competition simulates an unprivileged user with physical access to a keyboard and terminal attempting to gain local privilege escalation on an unfamiliar system.
>
>Documentation: https://github.com/sigpwny/pwnyOS-2020-docs/blob/master/Getting_Started.pdf
>
>System Calls: https://github.com/sigpwny/pwnyOS-2020-docs/blob/master/Syscalls.pdf
>
>For your first challenge: Login to the OS with username sandb0x
>
>Password is 4 characters, all lowercase letters. First character is 'p'. I wonder if there's a way to leak the next char, knowing that the first part of the password is right...?
>
>UPDATE ON DEPLOYMENT If your team was registered before midnight CDT on the first day of the competition, you may have received an email with your credentials. If those credentials do not work, or if you did not receive an email, please send us a modmail ASAP and we will get you set up as soon as possible.
>
>If you attempt to connect to another user's VM, or attempt to compromise challenge infrastructure in any way, you will be banned without warning.
>
>This challenge is the result of months of hard work- Please respect the challenge and don't attempt to ruin the experience for others.
>
>Author: ravi

Upon entering the credentials for the VNC server, we are greeted with a login page. 

![](https://github.com/matdaneth/uiuctf-writeups/blob/master/Images/time_to_start/kernel1.PNG?raw=true)

The challenge tells us that the username is sandb0x. Also, the challenge states that the password is four lowercase characters long, and that it starts with “p”. So, we start guessing. Our first guess is “pass”, one of the most common passwords. However, this doesn’t work. Then, considering that the name of the operating system is pwnyOS, we try the password “pwny”. It works!

![](https://github.com/matdaneth/uiuctf-writeups/blob/master/Images/time_to_start/kernel2.PNG?raw=true)

Flag: *uiuctf{timing_s1d3_chann3l_g4ng}*

(Note: this was not the intended solution; the intended solution, as hinted by the flag, was to notice that when a correct character was entered, the screen would delay a few seconds before saying “Incorrect login”.)
