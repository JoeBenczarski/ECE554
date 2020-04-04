import time
from jobs import *
from light_services import *

def main():
    servs = light_service()
    
    solids = [
        "Solid;1;0;255,0,0;\n",
        "Solid;1;0;255,0,0;0,255,0;\n",
        "Solid;1;0;255,0,0;0,255,0;0,0,255;\n",
        "Solid;1;0;255,0,0;0,255,0;0,0,255;0,255,255;\n",
        "Solid;2;0;255,0,0;\n",
        "Solid;2;0;255,0,0;0,255,0;\n",
        "Solid;2;0;255,0,0;0,255,0;0,0,255;\n",
        "Solid;2;0;255,0,0;0,255,0;0,0,255;0,255,255;\n",
        "Solid;3;0;255,0,0;\n",
        "Solid;3;0;255,0,0;0,255,0;\n",
        "Solid;3;0;255,0,0;0,255,0;0,0,255;\n",
        "Solid;3;0;255,0,0;0,255,0;0,0,255;0,255,255;\n",
        "Solid;4;0;255,0,0;\n",
        "Solid;4;0;255,0,0;0,255,0;\n",
        "Solid;4;0;255,0,0;0,255,0;0,0,255;\n",
        "Solid;4;0;255,0,0;0,255,0;0,0,255;0,255,255;\n",
        "Off;0;0;0,0,0;\n"
    ]
    
    pulses = [
        #"Pulse;0;0.2;255,0,0;0,255,0;\n",
        "Pulse;0;1;255,0,0;0,255,0;\n",
        "Off;0;0;0,0,0;\n"
    ]
    
    #shiftleft = "Shift Left;1;1;255,255,0;0,0,255;255,0,0;255,255,255;\n"
    #pulse = "Pulse;0;0.2;255,0,0;255,0,255;0,0,255\n"
    
    # test job parsing
    for msg in pulses:
        # test job parse
        j = job(msg)
        # test job process
        j.process(servs)
        time.sleep(1)
    
    pass
    

if __name__ == '__main__':
    main()
    