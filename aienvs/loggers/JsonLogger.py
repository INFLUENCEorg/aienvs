from aienvs.listener.Listener import Listener
import json
from _pyio import TextIOBase


class JsonLogger(Listener):
    
    """
    Logs final results coming from a DefaultRunner to a json file
    """
    
    def __init__(self, outstream: TextIOBase):
        """
        @param outstream a general outputstream, either file or StringIO.
        Create with  open("myfile.txt", "r", encoding="utf-8") or
        io.StringIO("some initial text data")
        """
        self._outstream = outstream
        
    def notifyChange(self, data):
        if data['done']:
            self._outstream.writelines(json.dumps(data))
        
