# 1Captcha

I spent a decent amount of time on this challenge actually trying to figure out what to do, but after going through the home page again, I noticed that it was a matter of a lowercase L versus a one. I loaded up Google Docs and noticed that the one was taller than the L (or vice versa, i forgot lol). I also noticed that the font size was the same throughout each Captcha. 

My solve path was to count and compare the amount of pixels per color. The background color would stay the same, so I took the color with the largest number of pixels and compared it with the other images. If it was the same, then the captcha would match. (Note, I also checked the second largest color to deal with random inconsistency). I then used the docs to create this solve script which would send requests.
