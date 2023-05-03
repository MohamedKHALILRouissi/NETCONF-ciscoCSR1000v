from ncclient import manager 
import xml.dom.minidom
# m represent the netconf remote session , in every 
# netconf session , the server first send its capabilities in list xml format
# the received list of capabilities is stored in the "m.server_capabilities" list
m = manager.connect(
    host="192.168.56.102",
    port=830,
    username="cisco",
    password="cisco123!",
    # if the host key_verify true the device will ask you to verify ssh fingerprint 
    hostkey_verify=False
    )

cap = input("would you like to get the netconf capability of cisco")
if cap == "yes":
    for i in m.server_capabilities:
        print(i)


netconf_filter= """
<filter>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""
netconf_hostname = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <hostname>R1</hostname>
 </native>
</config>
"""

withoutfilter = input("output all config")
if withoutfilter == "yes":
    config = m.get_config(source="running")
    print(xml.dom.minidom.parseString(config.xml).toprettyxml())


withfilter = input("output filterd config")
if withfilter == "yes":
    netconf_reply = m.get_config(source="running",filter=netconf_filter)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


editconfig = input("edit config")

if editconfig == "yes":
    netconf_reply = m.edit_config(target="running", config=netconf_hostname)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


loopback = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
 <interface>
 <Loopback>
 <name>1</name>
 <description>My first NETCONF loopback</description>
 <ip>
 <address>
 <primary>
 <address>10.1.1.1</address>
 <mask>255.255.255.0</mask>
 </primary>
 </address>
 </ip>
 </Loopback>
 </interface>
</native>
</config>
"""
loop = input("would you like to add loopback interface")

if loop == "yes":
    result = m.edit_config(target="running", config=loopback)
    print(xml.dom.minidom.parseString(result.xml).toprettyxml())
