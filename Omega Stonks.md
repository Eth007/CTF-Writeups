## Omega Stonks - 50 points - 25 solves

>If you solve this challenge, straightup you have Omega Stonks.
>
>(Buy this flag from IsabelleBot)

The solution we had for this challenge was VERY unintended. 

In this challenge it tells us that the flag for this challenge can be bought from the Isabelle bot. 

During the CTF, *someone* along the line decided that it would be a good idea to transfer negative money from to other people, to try to “steal” their bells. Most likely, the post got deleted, but the result was that FIREPONY57#0483 gained the ability to wield an infinite number of bells. 

After the CTF ended, it was revealed that this happened because of unsanitized input, and it ended up turning FIREPONY57#0483’s balance into some sort of string, effectively throwing a wrench into the system. In the end, his balance looked like this:

![](https://github.com/matdaneth/uiuctf-writeups/blob/master/Images/omega_stonks/writeup2.PNG?raw=true)

The bug in the bot apparently also brought up discussion among the admins, leading to the prize for most bells being removed. Several DMs asking for bells also were sent to FIREPONY57#0483. Of course, he refused all of them, after Pranav, the bot’s creator, told him to not transfer any more bells to others. 

![](https://github.com/matdaneth/uiuctf-writeups/blob/master/Images/omega_stonks/writeup3.PNG?raw=true)

From then on, FIREPONY57#0483’s balance kept on growing, and after some experimentation, he found out that he could transfer any amount of money to other people under 100999 bells. Only 5 of these transfers were needed to buy the flag. 

After transferring many bells to his teammate Eth007#0804, Eth007 could buy the flag, which was sent in a direct message. 

![](https://github.com/matdaneth/uiuctf-writeups/blob/master/Images/omega_stonks/writeup1.PNG?raw=true)

Flag: *uiuctf{so_much_money_so_much_time_enjoy_50_points_XD}*
