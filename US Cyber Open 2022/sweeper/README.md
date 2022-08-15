# sweeper - What happens when you unpickle untrusted data

> A twist on a classic game. Tread lightly while you dig up the flag.
>
> https://sweeper-w7vmh474ha-uc.a.run.app/
> 
> Author:  [Tsuto](https://github.com/jselliott)

`sweeper` was a web exploitation challenge in the US Cyber Open CTF in 2022, which is the first step toward qualification for the US Cyber Team. At the end of the CTF, it was worth 496 points and had 12 solves. 

## Initial Exploration
We visit the website and are greeted by a normal-looking minesweeper game. There are buttons on the top that let you to save a game and load a game from a save, which utilizes a game save file that is downloaded when a game is saved and uploaded when a game is loaded.

Opening a game save file, we see that it is base64 data. This had me stumped for a while, as there were many unprintable characters in the base64 output. I eventually guessed that this was a python pickle file, which is a file format for storing python serialized data. Loading this through `pickle.loads()` in a python shell, I get a python dictionary that represents the game state. The dictionary is huge, so I will not include it in this writeup, but it contains information about each mine in the game, and whether it has been flagged or cleared, as well as whether it has a mine or not and how many mines are nearby. Also, within the dictionary is a field for the `game_id` and information about how many mines there are.

One thing that we do know about python pickle files: never unpickle untrusted data. However, it appears that the website does exactly this when we load a save. 

## Why we should never unpickle untrusted data
The `pickle` documentation says:
> The  `pickle`  module  **is not secure**. Only unpickle data you trust.
> It is possible to construct malicious pickle data which will  **execute arbitrary code during unpickling**. Never unpickle data that could have come from an untrusted source, or that could have been tampered with.

Cool! Looks like we can do some remote code execution to read the flag!

I found that if I edited the game state dictionary by putting a new object in the `game_id` field, I would be able to read the string representation of the object. This is because `game_id` is returned to us through the websocket connection to the server on the client side after loading the game save.

So, all we need to do is construct an object that when unpickled, will return the output of a command we run or a file we open.

I tried to do this with the code below:
```python
from base64 import b64encode
from pickle import dumps
from functools import partial
from subprocess import check_output

class RCE(object):
    def __reduce__(self):
        return (partial(check_output, universal_newlines=True), (['cat', '/flag.txt'],))
```

I decided to use subprocess and functools because using `os.popen` or `open` would require me to call a method of the returned object in order to get a string returned (in this case `.read()`). So, my method uses functools to create a function object that will call `subprocess.check_output` with the parameter `universal_newlines=True` in order to make the function return a string rather than bytes. 

Replacing the `game_id` with this object, pickling it and encoding in base64, and uploading to the server as a game save file, we can get the flag through monitoring the websocket communications in our web browser's devtools: `USCG{f1ag5_4r3_a11_m1n3}`

Thanks to tsuto for a cool challenge!
