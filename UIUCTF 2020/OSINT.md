# OSINT Writeups

## Starter OSINT - 20 points - 95 solves

>Our friend isabelle has recently gotten into cybersecurity, she made a point of it by rampantly tweeting about it. Maybe you can find some useful information ;).
>
>While you may not need it, IsabelleBot has information that applies to this challenge.
>
>Finishing the warmup OSINT chal will really help with all the other osint chals
>
>The first two characters of the internal of this flag are 'g0', it may not be plaintext
>
>Made By: Thomas (I like OSINT)

Upon reading the challenge’s description, we find out that the Isabelle bot on Discord might just give us a hint. In the Discord Server, we find that the admins have put up a nickname for the Isabelle bot: "Hacker Isabelle".

![](Images/writeups1.PNG)

Because the challenge says that she was "rampantly tweeting about" her new interest in cybersecurity, we search Twitter for the name "Hacker Isabelle".

![](Images/writeups2.PNG)

Sure enough, we find a twitter account named “epichackerisabelle”, or "@hackerisabelle". 

![](Images/writeups3.PNG)

We search all her tweets and replies and we find, in plaintext, a flag.

![](Images/writeups4.PNG)

Flag: *uiuctf{g00d_w@rmup_y3s_Ye5}*

## Isabelle's Bad Opsec 1 - 40 points - 87 solves

>Isabelle has some really bad opsec! She left some code up on a repo that definitely shouldn't be public. Find the naughty code and claim your prize.
>
>**Finishing the warmup OSINT chal will really help with this chal**
>
>The first two characters of the internal of this flag are 'c0', it may not be plaintext_  _Additionally, the flag format may not be standard capitalization. Please be aware_
>
>Made By: Thomas


Looking at the Twitter account we found in “Starter OSINT”, we can then look through the posts. One of them seems interesting:

![](Images/writeups5.PNG)

We notice some phrases that Isabelle says a lot, such as “0x15ABE11E” and “mimidogz,” as shown in the pictures below.

![](Images/writeups7.PNG)
![](Images/writeups8.PNG)
![](Images/writeups9.PNG)
![](Images/writeups10.PNG)
![](Images/writeups11.PNG)
![](Images/writeups12.PNG)

So, we start searching on GitHub. A simple search of “0x15ABE11E” on GitHub yields the following repository:

![](Images/writeups13.PNG)

We open the repository "mimidogz", and we find nothing of interest, just some code to print a matrix and some weird dog esolang. 

![](Images/writeups14.PNG)

However, when we look at the commit history, we find an interesting commit. We see that a base64 encoded string was committed to the file "dogz.py" and then removed, with the content "dWl1Y3Rme2MwbU0xdF90b195b3VyX2RyM0BtNSF9==". 

![](Images/writeups15.PNG)

We decode this string, and we get the flag.

Flag: *uiuctf{c0mM1t_to_your_dr3@m5!}*

## Isabelle's Bad Opsec 2 - 40 points - 81 solves

>Wow holy heck Isabelle's OPSEC is really bad. She was trying to make a custom youtube api but it didnt work. Can you find her channel??
>
>**Finishing Isabelle's Opsec 1 will may you with this challenge**
>
>_The first two characters of the internal of this flag are 'l3', it may not be plaintext_  _Additionally, the flag format may not be standard capitalization. Please be aware_
>
>Made By: Thomas

In this challenge’s description, it tells us that Hacker Isabelle has made a really horrible YouTube api. On her github, we see that there is a repository called “api-stuff”:

![](Images/writeups16.PNG)

Once again, we look in the commit history. We see two interesting commits: “quickstart.go” and “quickstart.stop”. In the quickstart.stop commit, we see that there is a line of code with the following text:

![](Images/writeups17.PNG)

We can recognize this as a YouTube channel ID, which is at the end of the URL of every Youtube channel. In other words, every YouTube channel’s URL is in the following form:

    https://www.youtube.com/channel/[INSERT ID HERE]

 
Now that we have the channel ID, we navigate to [https://www.youtube.com/channel/UCnL8vVmpKY8ZmfSwoikavHQ](https://www.youtube.com/channel/UCnL8vVmpKY8ZmfSwoikavHQ), and we find that we have a YouTube channel with the name “EliteHackerIsabelle1337”. We can also see that the profile picture is the same as the one from the GitHub account and the Discord bot, so we know we are on the right track:

![](Images/writeups18.PNG)

We go to the “About” section on the channel, and we find that there are two links at the bottom of the page: one leading to Isabelle’s Twitter account and one leading to her website:

![](Images/writeups19.PNG)

Because we have already been to her twitter, we click the link to her website. It leads us to the UIUCTF homepage, but in the URL we can see that the flag is being sent as a GET request:

![](Images/writeups20.PNG)

We unescape the characters, and we get the flag.

Flag: *uiuctf{3g3nd_oF_zeld@_m0re_like_l3gend_0f_l1nk!}*

## Isabelle's Bad Opsec 3 - 80 points - 28 solves

>Isabelle has a youtube video somewhere, something is hidden in it.
>
>**Solving Previous OSINT Chals will help you with this challenge**
>
>The first two characters of the internal of this flag are 'w3', it may not be plaintext._  _Additionally, the flag format may not be standard capitalization. Please be aware_
>
>Made By: Thomas

We go to Isabelle's YouTube channel, and we find that she has one video, titled "[TUTORIAL 4.1.2519] how to involke mimidogz and pwn Arch Linux (GONE WRONG, MOM WAS ANGRY!!)":

![](Images/writeups21.PNG)

Thinking about what kind of data could be hidden in a video, we decide to start with the captions. However, when we look at the video with captions enabled, nothing shows up. So, we go to the "Add translations" function that YouTube provides. 

![](Images/writeups22.PNG)

In the translation draft, we find a flag, as well as some notes from other teams.

![](Images/writeups22b.PNG)

Flag: *uiuctf{w3_l0Ve_@nd_va1uE_oUR_c0mMun!ty}*

## Isabelle's Bad Opsec 4 - 100 points - 21 solves

>Isabelle hid one more secret somewhere on her youtube channel! Can you find it!?
>
>**Finishing previous OSINT Chals will assist you with this challenge**
>
>The first two characters of the internal of this flag are 'th', it may not be plaintext_
>
>_Additionally, the flag format may not be standard capitalization. Please be aware_
>
>Made By: Thomas [Authors Note]  _I love this chal because I used it IRL to find out who someone cyberbullying a friend was. It's real OSINT -Thomas_

First, we note that the author of this challenge has left a note, saying that this method was realistic, and that he used it in real life before. This suggests that he had some experience with the method, and he might have talked about it somewhere.

So, we go to SIGPwny's website at https://sigpwny.github.io/, and we find a link to their "Fall HACKathon" that they hosted last year. 

![](Images/writeups23.PNG)

At the page, we find the schedule of the event. As it turns out, each item on the schedule had a link to the slideshow used in that section.

![](Images/writeups24.PNG)

We click on the "Recon" link, because it is another word for OSINT.  Opening the slideshow, we find that we are in luck! The presentation was done by Thomas, who made this challenge! 

![](Images/writeups25.PNG)

On the last slide, we find tips for YouTube OSINT. 

![](Images/writeups26.PNG)

Near the middle of the slide, one of the tips reads:

>Youtube sends you the full banner image, not just the crop.

This trick seems realistic enough, because you could use an uncropped YouTube banner to find someone's identity. So, we try this trick on Isabelle's channel. We use [https://mattw.io/youtube-metadata/](https://mattw.io/youtube-metadata/) to find the links to all the banner images that YouTube keeps on the video. (You can visit https://mattw.io/youtube-metadata/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DdjhRaz3viU8&submit=true to see my results on this channel.) 

In the "Branding Settings" tab, we find that YouTube has various links for the channel banner. On the bottom one, titled "bannerTvHighImageUrl", we find the uncropped image.

![](Images/writeups27.jpg)

At the bottom of the image, we find the flag.

Flag: *uiuctf{this_flag_is_not_cake_on_the_inside}*


## Isabelle's Bad Opsec 5 - 100 points - 32 solves

> Isabelle had one more secret on her youtube account, but it was embarrassing.
>
>**Finishing previous OSINT Chals will assist you with this challenge**
>
>The first two characters of the internal of this flag are 'hi', it may not be plaintext_
>
>**The flag capitalization may be different, please be aware**

Upon reading the challenge description, it says that Isabelle *had* (note the past tense) one more secret on her YouTube account. Also, the description says that the secret was "embarrasing." This all hints at the flag being deleted. 

The way we can view content on the internet that was deleted is to use the Internet Archive's Wayback Machine, which contains snapshots of websites from the past. Anyone can take a snapshot, so the challenge author might have made a snapshot of the channel sometime in the past. 

When we look up the "About" page on Isabelle's channel, we find that a snapshot was taken on July 14th, several days before the CTF. 

![](Images/writeups30.PNG)

This is just right for the challenge, because we remember that on that date, Thomas(the challenge author) had posted about the OSINT challenges not being done at https://discordapp.com/channels/722150434566963293/722150435137388609/732729060211556482 .

![](Images/writeups29.PNG)

We navigate to the snapshot, and we find that the Twitter link at the bottom has been removed, and that the website link has been edited. 

![](Images/writeups32.PNG)

We go to the website link, and we find that as before, the flag has been sent as a GET request. 

![](Images/writeups33.PNG)

(Note: we were actually the third team to solve this challenge, and we solved it *before* we solved Isabelle's Bad Opsec 1.)

Flag: *UIUCTF{hidd3n_buT_neVeR_g0n3}*
