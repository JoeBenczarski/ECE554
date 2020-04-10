/*************************************************************************/
/*  File Name:  SendToRPIButtonListener.java                             */
/*  Purpose:    Listener for the "send to RPI" button.                   */
/*  Created by: Darren Cicala on 21/03/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/
package com.example.light_controller;

/******************************* imports *********************************/
import android.content.Context;
import android.graphics.Color;
import android.view.View;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class SendToRPIButtonListener implements Button.OnClickListener
{
    OutputStream os;  // output bluetooth stream, sent over from the main activity
    InputStream  is;  // input bluetooth stream, also sent over from the main activity

    final int BUFFER_SIZE = 3;              // maximum return string size
    byte[] buffer = new byte[BUFFER_SIZE];  // byte buffer for reading from the bluetooth bus
    BluetoothMessageClass bluetoothMessage; // message to send to the raspberry pi
    Spinner lightType, numLEDs, frequency;
    Context context;
    Button connectButton;
    Button[] colorButtons = new Button[4];

    /* class constructor. Creates local copies of the input and output streams. */
    public SendToRPIButtonListener(OutputStream os, InputStream is, BluetoothMessageClass bluetoothMessage, Spinner lightType, Spinner numLEDs, Spinner frequency, Context context, Button connectButton, Button[] colorButtons)
    {
        this.os = os;
        this.is = is;
        this.bluetoothMessage = bluetoothMessage;

        this.lightType = lightType;
        this.numLEDs   = numLEDs;
        this.frequency = frequency;
        this.context   = context;

        this.connectButton = connectButton;
        this.colorButtons  = colorButtons;
    }

    /* this function gets called when the button is pressed  */
    @Override
    public void onClick(View v)
    {
        try
        {
            bluetoothMessage.SetFrequency(Double.valueOf(this.frequency.getSelectedItem().toString()));
            bluetoothMessage.SetLightType(this.lightType.getSelectedItem().toString());
            bluetoothMessage.SetNumLEDs(Integer.valueOf(this.numLEDs.getSelectedItem().toString()));

            bluetoothMessage.ConstructCSVStr();
            this.write(bluetoothMessage.stringToTransmit);
            this.read();

            String temp = new String(buffer);
            if(temp.equals("ACK"))
            {
                Toast.makeText(context, "Message successfully transmitted.", Toast.LENGTH_LONG).show();
            }
        }
        /* error handling */
        catch(IOException e)
        {
            Toast.makeText(context, "Connection terminated. Please reconnect!", Toast.LENGTH_LONG).show();
            connectButton.setText("CONNECT");
            connectButton.setBackgroundColor(Color.rgb(255,0,0));
            e.printStackTrace();
        }
    }

    /* write a string to the output stream (bluetooth socket) */
    public void write(String s) throws IOException
    {
        byte[] x = s.getBytes();
        os.write(x);
    }

    /* read a string from the input stream (bluetooth socket) */
    public void read()
    {
        int bytes = 0;
        int b = BUFFER_SIZE;
        //while (true)
        //{
            try
            {
                bytes = is.read(buffer, bytes, BUFFER_SIZE - bytes);
                //break;
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
       // }
    }
}
