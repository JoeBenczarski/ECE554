# ECE554

To run the android application on an emulator:
1. Download and install Android Studio.
2. Select open an existing android studio project.
3. Select Android_Application within the extracted zip file.
4. Create an emulated device using the AVD manager (Pixel 2 will suffice), or
5. a) Open your settings and find the build number (will most likely be  Settings > About Phone > Build Number)

   b) Tap the build number seven times to enable developer options.
   
   c) Enable USB debugging (can most likely be found at Settings > System > Advanced > Developer Options > USB debugging)
   
   d) Connect your phone to your computer using a USB cable.
   
   e) Source: https://developer.android.com/studio/debug/dev-options
   
6. Select your device from step 4 or step 5 as the emulated device, by checking the dropdown in the top-center portion of the screen.
7. Run the program, by pressing the green triangle next to the dropdown from step 6. The application will deploy to your device.

*Please note the bluetooth functionality is only available if the application is implemented on an actual smartphone*

To run the Raspberry Pi code on a Raspberry Pi:
1. Open command prompt and install BlueZ bluetooth protocol stack using the command: sudo apt-get install bluetooth blueman bluez
2. Reboot the Raspberry Pi.
3. Open command prompt and access the file located at location: /etc/systemd/system/dbus-org.bluez.service
4. Add a compatability flag next to the existing line and on a separate line add a serial port profile.
5. Save the file.
6. Install pybluez python library to interface with BlueZ service: sudo apt-get install libbluetooth-dev
                                                                   sudo apt-get install python-dev
                                                                   sudo pip install PyBluez
7. Enable the SPI bus within the command prompt utilizing: sudo raspi-config 
8. Install light libraries within the command prompt utilizing: sudo apt-get update 
                                                                sudo apt-get install python-pip -y
                                                                sudo pip install adafruit-ws2801
9. Install asyncio library within the command prompt utilizing: pip install asyncio
10. Ensure bluetooth is discoverable on the pi.
11. Run the python script main located within RaspberryPi/Source/v2

*Please note, to enable the script to run on startup of the pi you must edit: sudo nano /etc/rc.local
within this area add the python script (e.g. sudo python3 /home/pi/sample.py &) after this reboot the pi*
