from flask import Flask,jsonify,request,Response,json
import threading,paramiko
import psutil

app = Flask(__name__)
app.config["DEBUG"] = True

def read_server_json():
    jsonHandler=open("../runtime_server.json")
    servers_json = json.load(jsonHandler)
    # {'servers': [{'id': 1, 'ip': '127.0.0.1', 'port': 5010, 'active': 0, 'health': 1, 'applications': 0}, {'id': 2, 'ip': '127.0.0.1', 'port': 5011, 'active': 0, 'health': 1, 'applications': 0}, {'id': 3, 'ip': '127.0.0.1', 'port': 5012, 'active': 0, 'health': 1, 'applications': 0}]}
    return servers_json

def return_servers():
    servers=list()
    serversjson = read_server_json()
    for i in serversjson:
        servers.append(i["ip"])
    #[127.0.0.1,127.0.0.1,127.0.0.1]
    return servers

def runtime_servers_datagather():
    myjson=read_server_json()
    all_runtimeservers=return_servers()
    i=0
    capacity=dict()
    tmp=[]
    
    for server in all_runtimeservers:
        #capacity[myjson["servers"][i]["id"]]=server
        #capacity["applications"]=myjson["servers"][i]["applications"]
        _user=myjson[i]["username"]
        _pass=myjson[i]["password"]
        tmp_dict=dict()

        """#uncomment this code if you want to get perform metrics from run time server
           #using ssh and remember user name password is fetched from runtime_server.json
        client =paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=server,username=_user,password=_pass)
        _ftp=client.open_sftp()
        _ftp.put("stats.py","stats.py")
        _ftp.close()
        stdin, stdout, stderr = client.exec_command("/usr/local/bin/python3 stats.py")
        for line1 in stdout:
            print(line1.strip())
            tmp.append(line1.strip())
        client.close() 
        """
        tmp.append(psutil.cpu_times_percent(interval=1).idle)
        tmp.append(psutil.virtual_memory().percent)

        tmp_dict["host"]=server
        tmp_dict["port"]=myjson[i]["port"]
        tmp_dict["applications"]=myjson[i]["applications"]
        tmp_dict["idle_cpu"]=float(tmp[0])
        tmp_dict["used_mem"]=float(tmp[1])
        capacity[myjson[i]["id"]]=tmp_dict
        i=i+1
    #print(capacity)
    #{'server1': {'host': '127.0.0.1', 'port': 5010, 'applications': 0, 'idle_cpu': 80.6, 'used_mem': 53.4}, 'server2': {'host': '127.0.0.1', 'port': 5011, 'applications': 0, 'idle_cpu': 80.6, 'used_mem': 53.4}, 'server3': {'host': '127.0.0.1', 'port': 5012, 'applications': 0, 'idle_cpu': 80.6, 'used_mem': 53.4}}
    return capacity

def deploy_here_loadbalancer():
    capacity = runtime_servers_datagather()
    create_new=False
    #('server1', {'host': '127.0.0.1', 'port': 5010, 'applications': 0, 'idle_cpu': 80.6, 'used_mem': 53.4})
    for server in capacity.items():
        if(server[1]['applications']>2 or server[1]['idle_cpu']<30 or server[1]['used_mem']>80):
            create_new=True
            continue
        elif(server[1]['applications']<=2 and server[1]['idle_cpu']>30 and server[1]['used_mem']<80):
            return server[1]['host'],server[1]['port']
    if(create_new):
        print("#call ronit function to create server")
        

def running_runtime():
    ip,port=deploy_here_loadbalancer()
    return_status=dict()
    return_status["host"]=ip
    return_status["port"]=port
    return return_status

@app.route("/servermanager/assign_runtime_server/")

def running_runtime():
    ip,port=deploy_here_loadbalancer()
    return_status=dict()
    return_status["host"]=ip
    return_status["port"]=port

    server_allocation_status = Response(json.dumps(return_status), status=200, mimetype='application/json')
    return server_allocation_status


if __name__ == "__main__":
    app.run(port=4999)

