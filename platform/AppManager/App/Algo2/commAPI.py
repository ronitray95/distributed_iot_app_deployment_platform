import time
import comm_module as cm

class comm(object):
    def __init__(self):
        pass

    def handler_function(self, msg):
        msg = msg.value["data"]
        return msg

    def getData(self, id):
        
        data = {"msg":id}
        cm.send_message("Deployer_to_SM_data",data)
        return cm.consume_msg('SM_to_Deployer_data',self.handler_function)


    def setData(self, type, loc, value):

        data = {"msg":[type, value]}
        cm.send_message("AS",data)
        return cm.consume_msg('AS',self.handler_function)


    def sendNotification(self, msg):
        pass

obj = comm()