#!/usr/bin/env bash

# trap "exit" INT TERM ERR
# trap "kill 0" EXIT

#Initiating Kafka server
gnome-terminal -x ./kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties
sleep 2
gnome-terminal -x ./kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties

cd platform/AppManager
gnome-terminal -x ./appManager.py
cd ..

cd AppServiceManager
gnome-terminal -x ./node_manager.py
gnome-terminal -x ./appService.py
gnome-terminal -x ./logger.py
cd ..

cd scheduler
gnome-terminal -x ./scheduler.py
cd ..

cd SensorManager
gnome-terminal -x ./sensor_services.py
gnome-terminal -x ./init.py


#Registering Kafka topics
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic AS &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic DS &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic SM_to_Deployer_get &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic Deployer_to_SM_data &
#  .~/kafka/bin/./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic SM_to_Deployer_data &

# Initiating modules
# python3 ~/vscode/platform/Hackathon2_AppManager/appManager.py &

# python3 ~/vscode/platform/AppServerManager/node_manager.py &

# python3 ~/vscode/platform/AppServerManager/deployment.py&

# python3 ~/vscode/platform/SensorManager/init.py &

# python3 ~/vscode/platform/scheduler/scheduler.py





# # cd Service_Lifecycle
# sudo python3 platform/Service_Lifecycle/service_lifecycle.py &
# # cd ..


# # cd Server_Lifecycle
# sudo python3 platform/Server_Lifecycle/server_lifecycle.py &
# # cd ..


# # cd Deployment_Manager
# sudo python3 platform/Deployment_Manager/DeploymentManager.py &
# # cd ..


# # cd SensorManager
# sudo python3 platform/SensorManager/SensorManager.py &
# # cd ..

# # cd Action_Manager
# sudo python3 platform/Action_Manager/actionserver.py &
# # cd ..

# # cd Scheduler
# sudo python3 platform/Scheduler/sched.py &
# cd ..

# wait