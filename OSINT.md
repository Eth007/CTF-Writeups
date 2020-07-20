## Starter OSINT

> Our friend isabelle has recently gotten into cybersecurity, she made a
> point of it by rampantly tweeting about it. Maybe you can find some
> useful information ;). While you may not need it, IsabelleBot has
> information that applies to this challenge. Finishing the warmup OSINT
> chal will really help with all the other osint chals The first two
> characters of the internal of this flag are 'g0', it may not be
> plaintext Made By: Thomas (I like OSINT)

Upon reading the challenge’s description, we find out that the Isabelle bot on Discord might just give us a hint. In the Discord Server, we find that the admins have put up a nickname for the Isabelle bot: "Hacker Isabelle".

[insert picture of nickname]

Because the challenge says that she was "rampantly tweeting about" her new interest in cybersecurity, we search Twitter for the name "Hacker Isabelle".

[insert picture of search]

Sure enough, we find a twitter account named “epichackerisabelle”, or "@hackerisabelle". 

[insert picture of profile]

We search all her tweets and replies and we find, in plaintext, a flag.

[insert picture of post]

Flag: *uiuctf{g00d_w@rmup_y3s_Ye5}*

## Isabelle's Bad Opsec 1


Looking at the Twitter account we found in “Starter OSINT”, we can then look through the posts. One of them seems interesting:

[insert picture of github reference]

We notice some phrases that Isabel says a lot, such as “0x15ABE11E” and “mimidogz,” as shown in the pictures below.

[insert pictures of posts]

So, we start searching on GitHub. A simple search of “0x15ABE11E” on GitHub yields the following repository:

[insert picture of search page]

We open the repository "mimidogz", and we find nothing of interest, just some code to print a matrix and some weird dog esolang. 

[insert picture]

However, when we look at the commit history, we find an interesting commit. We see that a base64 encoded string was committed to the file "dogz.py" and then removed, with the content "dWl1Y3Rme2MwbU0xdF90b195b3VyX2RyM0BtNSF9==". 

[insert picture]

We decode this string, and we get the flag.

Flag: *uiuctf{c0mM1t_to_your_dr3@m5!}*

## Isabelle's Bad Opsec 2

In this challenge’s description, it tells us that Hacker Isabelle has made a really horrible youtube api. On her github, we see that there is a repository called “api-stuff”:

[insert picture]

Once again, we look in the commit history. We see two interesting commits: “quickstart.go” and “quickstart.stop”. In the quickstart.stop commit, we see that there is a line of code with the following text:

    This channel's ID is UCnL8vVmpKY8ZmfSwoikavHQ. Its title is '%s' 

We can recognize this as a YouTube channel ID, which is at the end of the URL of every Youtube channel. In other words, every YouTube channel’s URL is in the following form:

    https://www.youtube.com/channel/[INSERT ID HERE]

 
Now that we have the channel ID, we navigate to [https://www.youtube.com/channel/UCnL8vVmpKY8ZmfSwoikavHQ](https://www.youtube.com/channel/UCnL8vVmpKY8ZmfSwoikavHQ), and we find that we have a YouTube channel with the name “EliteHackerIsabelle1337”. We can also see that the profile picture is the same as the one from the GitHub account and the Discord bot, so we know we are on the right track:

[insert picture]

We go to the “About” section on the channel, and we find that there are two links at the bottom of the page: one leading to Isabelle’s Twitter account and one leading to her website:

[insert picture]

Because we have already been to her twitter, we click the link to her website. It leads us to the UIUCTF homepage, but in the URL we can see that the flag is being sent as a POST request:

[insert picture]

We unescape the characters, and we get the flag.

Flag: *uiuctf{3g3nd_oF_zeld@_m0re_like_l3gend_0f_l1nk!}*
