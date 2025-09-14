"""
mqtt-poly-pg3x NodeServer/Plugin for EISY/Polisy

(C) 2024

node MQDroplet
"""

import udi_interface
import json

LOGGER = udi_interface.LOGGER

class MQDroplet(udi_interface.Node):
    id = 'mqdrop'
    
    """
    This is the class that all the Nodes will be represented by. You will
    add this to Polyglot/ISY with the interface.addNode method.
    """

    def __init__(self, polyglot, primary, address, name, device):
        """
        Super runs all the parent class necessities.
        :param polyglot: Reference to the Interface class
        :param primary: Parent address
        :param address: This nodes address
        :param name: This nodes name
        """
        super().__init__(polyglot, primary, address, name)
        self.controller = self.poly.getNode(self.primary)
        self.cmd_topic = device["cmd_topic"]
        self.on = False
        self.motion = False
        self.qrypaylaod = ""

    def updateInfo(self, payload, topic: str):
        try:
            data = json.loads(payload)
        except Exception as ex:
            LOGGER.error("Failed to parse MQTT Payload as Json: {} {}".format(ex, payload))
            return False

        
        
        # flow
        if "flow" in data:
            self.setDriver("GV5", data["flow"])
        # signal
        if "signal" in data:
            if data["signal"] == "No Signal":
                value = 1
            elif data["signal"] == "Weak Signal":
                value = 2
            elif data["signal"] == "Strong Signal":
                value = 3
            else:
                value = 0
            self.setDriver("GV6", value)  
         # server
        if "server" in data:
            if data["server"] == "Connecting":
                value = 1
            elif data["server"] == "Connected":
                value = 2
            else:
                value = 0
            self.setDriver("GV7", value)     
            
    def query(self, command=None):
        """
        Called by ISY to report all drivers for this node. This is done in
        the parent class, so you don't need to override this method unless
        there is a need.
        """
        self.qrypayload = "{"Online": 1}"
        LOGGER.debug(f"payload: {self.qrypayload}")
        self.controller.mqtt_pub(self.cmd_topic, qrypayload)
        LOGGER.debug(f"cmd_topic: {self.cmd_topic}")
        self.reportDrivers()
        
    # all the drivers - for reference
    drivers = [       
        
        {"driver": "GV5", "value": 0, "uom": 130},
        {"driver": "GV6", "value": 0, "uom": 25},
        {"driver": "GV7", "value": 0, "uom": 25},
        ]

    """
    This is a dictionary of commands. If ISY sends a command to the NodeServer,
    this tells it which method to call. DON calls setOn, etc.
    """
    commands = {
        "QUERY": query        
        }
