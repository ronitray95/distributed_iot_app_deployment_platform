import API
import time

api = API.sensorapi()
api.display(f'{time.ctime()} :: Email sent to {api.getEmailID()}')
api.sendMail('sdsd',f'{time.ctime()} :: Email sent to {api.getEmailID()}') 