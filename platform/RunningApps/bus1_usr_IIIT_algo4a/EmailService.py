import API
import time

api = API.sensorapi()
api.display(f'{time.ctime()} :: Email sent to {api.getEmailID()}')
msg = str(time.ctime())+' :: Email sent to '+ str(api.getEmailID())
api.sendMail(msg) 