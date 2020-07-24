## Feedback Survey - 20 points - 109 solves

>Please fill out the feedback survey here! https://forms.gle/qfWGeN6jFf5kRcZW8

We see that this challenge tells us to fill out the survey. We go on ahead and click the link. 

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/survey.PNG)

We are familiar with CTFs asking us to fill out a survey to improve their CTF for the next year. We see some questions and start filling them up when then we get to the last 2 questions. 

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/2questions.PNG)

They seem… different. They require us to write down an answer and give them comments. We think about it for a few moments and just write nothing. After all, it’s just a survey. We press the submit button and expect to get a flag, but we get none. (Afterthought: this was when they forgot to put the flag after the survey)

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/done.jpg)

We wonder what we did wrong. In most CTFs they give us the flag right after we finish the survey. Then we remember another challenge named “Spoockies”. It was worth 20 points, but it was actually pretty hard. The feedback survey must be one of those challenges! (Afterthought: Sprookies wasn’t hard, we just don’t have the capability to do pwn...)

Then we remember that we left the last two questions blank! It must be that we have to put a certain answer in the last two questions to get the flag! Even though it seems awfully guessy, we keep editing our last 2 answers and submitting them, hoping to get a flag. In the middle of trying to guess the input, one of my teammates decided to ask for the flag. So in the middle of my guessing we get a DM from Thomas. We look at the DM and we see this:

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/dm.PNG)

It looks like the admin really appreciates that we actually found out what we have to do to get the flag. Well, back to our input brute-forcing. We continue trying to guess it when we realize it's hopeless. There are SOOOOOOO many possibilities for what it could be. (Afterthought: more like infinity) We start to give up like we did with Spoockies. (we never did get around to solving that… oops... ) We then realize that the Admins could have hidden the flag anywhere. We try taking the first letter of all the questions, but we just come up with this weird string: WWOHWWWWAWWA. We are about to disregard this as a distraction when we realize something. If we actually sound it out, it seems to be saying: WOWA. The admins are wowing at us! That must mean that we are on the right track. We think that maybe this might actually be the flag! We try to submit it, but… again we are wrong.

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/badflag.PNG)

Then we realize another thing. WOWWW can also mean that they are wowing at how stupid we are being. Then we realize that we are really being stupid and stop our search. We go back to the message Thomas sent us to see if he might have given us a hint. We then notice a uiuctf in front of the message! We realize the flag might have been just encrypted and he gave it to us!(Since the admins forgot to add the flag after the survey, they sent the flag to the people who already did the survey) We try Using caesar cipher shift 26, but it just spits out the same thing

![](https://raw.githubusercontent.com/matdaneth/uiuctf-writeups/master/Images/feedback_survey/caesar.PNG)

So we try using ROT-13 TWENTY-SIX times to get the decrypted flag, but it still spits out the same thing. (go to the CyberChef link below if you don’t believe me. This is crazy!)

https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)ROT13(true,true,13)&input=dWl1Y3Rme3lvdXJfaW5wdXRfaXNfaW1wb3J0YW50X3RvX3VzfQ

We keep thinking of other ciphers that may have encrypted the flag when we realize yet another thing. If the uiuctf is there in plain text, then the rest of the flag is in plain text! We look at it and submit the flag and we get it right! Then we just sit there happily looking at our team having raised ZERO whole places in the CTF.

Flag: [*uiuctf{your_input_is_important_to_us}*](https://www.youtube.com/watch?v=oHg5SJYRHA0)

(gotcha.)
