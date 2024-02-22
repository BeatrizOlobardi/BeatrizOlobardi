import paho.mqtt.client as mqtt

host_mqtt = "10.1.0.18" 
porta_mqtt = 1883 

def requestIMUStream():
    client.publish('cmd2dev9840','{"op":1,"simulationTime":"3",'+
                    '"frequence":10,"sensorType":2}')
def stopIMU():
    client.publish('dev9840ss',{'op':22})

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))
    client.subscribe("newdev")
    client.subscribe("dev9840ss")
    requestIMUStream()

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    posicao_pri = str(msg.payload).find(',')
    posicao_pro = str(msg.payload).find(',', posicao_pri + 1)
    print(str(msg.payload)[posicao_pri+1:posicao_pro])

    if str(msg.payload)[posicao_pri+1:posicao_pro] > '0.93':
        print("Foi")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,1,0",' +
     
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}') 
        print("N foi")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}')

    if msg.topic == "dev9840ss":
        client.publish("seu_topico_de_saida", msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("0.tcp.sa.ngrok.io:16896", porta_mqtt, 60)

client.loop_start()
