/*************************************************************************/
/*  File Name:  MainActivity.java                                        */
/*  Purpose:    Main activity for the light controller application.      */
/*  Created by: Darren Cicala on 21/03/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/

package com.example.light_controller;

/******************************* imports *********************************/
import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.graphics.Color;
import android.os.ParcelUuid;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.os.Bundle;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;

public class MainActivity extends AppCompatActivity
{

    /* layout objects */
    SeekBar  redSlider;                        // red slider (R of RGB, range 0-255)
    SeekBar  greenSlider;                      // green slider (G of RGB, range 0-255)
    SeekBar  blueSlider;                       // blue slider (b of RGB range 0-255)
    Button   addColorButton;                   // button to add the color to the current list
    Spinner  lightTypeSpinner;                 // dropdown to determine what kind of light to show (solid, pulse, shift)
    Spinner  frequencySpinner;                 // dropdown to determine what frequency to use (1-10 Hz range)
    Spinner  numLEDSpinner;                    // number of LEDs for each color in the sequence
    Button   sendToRPIButton;                  // button to send the data over bluetooth to the raspberry pi
    Button[] colorButtons = new Button[4];     // list of buttons to assign colors to
    Button   cancelButton;                     // button to clear the current configuration
    Button   connectButton;                    // button to establish connection to a bluetooth device

    /* bluetooth communication objects */
    BluetoothMessageClass bluetoothMessage;   // container class to store all of the relevant fields of the bluetooth message
    BluetoothSocket socket;                   // global bluetooth socket
    public OutputStream outputStream;         // outgoing stream, for sending data TO the pi
    public InputStream inStream;              // incoming stream, for receiving data FROM the pi
    int raspberryPiIndex = 0;                 // index of the raspberry pi in the "paired devices" section of your phone


    /*************************************************************************/
    /*  Function Name: onCreate                                              */
    /*  Purpose:       Function that gets called once each time the app      */
    /*                 restarts.                                             */
    /*************************************************************************/
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        /* initialize application view */
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /* get references to each of the layout objects from the resource XML */
        redSlider        = (SeekBar) findViewById(R.id.seekBarRed);
        greenSlider      = (SeekBar) findViewById(R.id.seekBarGreen);
        blueSlider       = (SeekBar) findViewById(R.id.seekBarBlue);
        addColorButton   = (Button) findViewById(R.id.addColorButton);
        sendToRPIButton  = (Button) findViewById(R.id.sendToRPI);
        lightTypeSpinner = (Spinner) findViewById(R.id.lightType);
        frequencySpinner = (Spinner) findViewById(R.id.frequencySpinner);
        numLEDSpinner    = (Spinner) findViewById(R.id.numberLEDs);

        colorButtons[0] = (Button) findViewById(R.id.color1);
        colorButtons[1] = (Button) findViewById(R.id.color2);
        colorButtons[2] = (Button) findViewById(R.id.color3);
        colorButtons[3] = (Button) findViewById(R.id.color4);
        cancelButton    = (Button) findViewById(R.id.cancelButton);
        connectButton   = (Button) findViewById(R.id.connectButton);


        /* create a new instance of the bluetooth message on startup */
        bluetoothMessage = new BluetoothMessageClass();

        /* color picker configuration */
        SeekBarListener localSeekBarListener = new SeekBarListener(addColorButton, redSlider, greenSlider, blueSlider);
        redSlider.setOnSeekBarChangeListener(localSeekBarListener);
        greenSlider.setOnSeekBarChangeListener(localSeekBarListener);
        blueSlider.setOnSeekBarChangeListener(localSeekBarListener);

        CancelButtoniListener cancelListener = new CancelButtoniListener(redSlider, greenSlider, blueSlider, lightTypeSpinner, frequencySpinner, numLEDSpinner, colorButtons, bluetoothMessage);
        cancelButton.setOnClickListener(cancelListener);

        /* add color button press configuration  */
        AddColorButtonListener localButtonListener = new AddColorButtonListener(redSlider, greenSlider, blueSlider, bluetoothMessage, colorButtons, this.getApplicationContext());
        addColorButton.setOnClickListener(localButtonListener);

        ConnectButtonListener connectListener = new ConnectButtonListener(this, this);
        connectButton.setOnClickListener(connectListener);
        connectButton.setBackgroundColor(Color.rgb(255,0,0));

        /* spinner (dropdown) configuration */
        ArrayAdapter<CharSequence> lightTypeAdapter = ArrayAdapter.createFromResource(this, R.array.light_options, android.R.layout.simple_spinner_dropdown_item);
        ArrayAdapter<CharSequence> frequencyAdapter = ArrayAdapter.createFromResource(this, R.array.Frequency, android.R.layout.simple_spinner_dropdown_item);
        ArrayAdapter<CharSequence> numLEDAdapter = ArrayAdapter.createFromResource(this, R.array.numLEDs, android.R.layout.simple_spinner_dropdown_item);

        lightTypeSpinner.setAdapter(lightTypeAdapter);
        frequencySpinner.setAdapter(frequencyAdapter);
        numLEDSpinner.setAdapter(numLEDAdapter);

        /* print a "finished" message */
        System.out.println("###### Initialization Finished ####### ");
    }

    /*************************************************************************/
    /*  Function Name: BluetoothInit                                         */
    /*  Purpose:       Function to set up the bluetooth socket's variables.  */
    /*  Note:          Based on eleven's post on Stack Overflow:             */
    /*                 https://stackoverflow.com/a/22899728                  */
    /*************************************************************************/
    private void BluetoothInit(int index) throws IOException
    {
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter != null)
        { // there is a bluetooth adapter on this device

            if (blueAdapter.isEnabled())
            { // the bluetooth adapter is enabled

                /* get a list of all bluetooth devices paired to this phone */
                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();
                if(bondedDevices.size() > 0)
                { // there are some bonded devices to this phone

                    Object[] devices = (Object []) bondedDevices.toArray();                 // cast this list to an indexable array
                    BluetoothDevice device = (BluetoothDevice) devices[index];              // get the specific desired index of the paired bluetooth device (in this case, 6)
                    ParcelUuid[] uuids = device.getUuids();                                 // get the bluetooth UUID from the device
                    socket = device.createInsecureRfcommSocketToServiceRecord(uuids[0].getUuid());  // then use this UUID to initialize the global bluetooth socket
                    socket.connect();                                                       // connect the socket
                    outputStream = socket.getOutputStream();                                // initialize the output stream
                    inStream = socket.getInputStream();                                     // initialize the input stream
                    System.out.println("##### Socket successfully intialized. ##### ");
                }
                else
                {
                    Log.e("error", "No appropriate paired devices.");
                }
            }
            else
            {
                Log.e("error", "Bluetooth is disabled.");
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent)
    {
        super.onActivityResult(requestCode, resultCode, intent);
        if(requestCode == 0)
        {
            try
            {
                int index = intent.getIntExtra("deviceID", 0);
                try
                {
                    this.BluetoothInit(index);
                    connectButton.setBackgroundColor(Color.rgb(0,255,0));
                    connectButton.setText("CONNECTED");

                    /* send configuration to rpi button configuration */
                    SendToRPIButtonListener localSendListener = new SendToRPIButtonListener(outputStream, inStream, bluetoothMessage, lightTypeSpinner, numLEDSpinner, frequencySpinner, this.getApplicationContext(), connectButton, colorButtons);
                    sendToRPIButton.setOnClickListener(localSendListener);
                    bluetoothMessage = new BluetoothMessageClass();

                }
                catch (IOException e)
                {
                    Toast.makeText(this, "Could not connect to device, please try again", Toast.LENGTH_LONG).show();
                }
            }
            catch(NullPointerException e)
            {
                Toast.makeText(this, "Warning: No device selected", Toast.LENGTH_LONG).show();
            }
        }
    }
}
