from test.LoggedTestCase import LoggedTestCase
from aienvs.loggers.JsonLogger import JsonLogger
from unittest.mock import Mock


class test_JsonLogger(LoggedTestCase):
    
    def    test_log(self):
        logoutput = Mock()
        logger = JsonLogger(logoutput)
        
        data = {'done':True, 'actions':None}
        datajson = '{"done": true, "actions": null}'
        
        logger.notifyChange(data)

        logoutput.writelines.assert_called_with(datajson)
