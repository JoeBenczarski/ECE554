/*************************************************************************/
/*  File Name:  AddColorButtonListener.java                              */
/*  Purpose:    Listener for the "add color to list" button.             */
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
import android.widget.SeekBar;
import android.widget.Toast;

public class AddColorButtonListener implements Button.OnClickListener
{
    SeekBar redSeekBar, greenSeekBar, blueSeekBar; // local references of the color picker seekbars
    BluetoothMessageClass bluetoothMessage;        // local reference of the bluetooth message to send
    Button[] colorButtons = new Button[4];         // local references of color buttons
    Context context;

    /* constructor, creates local references of passed-in variables */
    public AddColorButtonListener(SeekBar redSeekBar, SeekBar greenSeekBar, SeekBar blueSeekBar, BluetoothMessageClass bluetoothMessage, Button[] colorButtons, Context context)
    {
        this.redSeekBar   = redSeekBar;
        this.greenSeekBar = greenSeekBar;
        this.blueSeekBar  = blueSeekBar;
        this.bluetoothMessage = bluetoothMessage;

        this.context = context;

        int i = 0;
        for(i=0;i<4;i++)
        {
            this.colorButtons[i] = colorButtons[i];
        }
    }

    /* called when the "add color" button is pressed */
    @Override
    public void onClick(View v)
    {
        int index = this.bluetoothMessage.numColors;
        if(index > 3)
        {
            Toast.makeText(context, "Too many colors!", Toast.LENGTH_LONG).show();
        }
        else
        {
            this.colorButtons[index].setBackgroundColor(Color.rgb(this.redSeekBar.getProgress(), this.greenSeekBar.getProgress(), this.blueSeekBar.getProgress()));

            /* add the color to the list of colors */
            this.bluetoothMessage.AddColor(this.redSeekBar.getProgress(), this.greenSeekBar.getProgress(), this.blueSeekBar.getProgress());

            /* reset the sliders to 0 */
            this.redSeekBar.setProgress(0);
            this.greenSeekBar.setProgress(0);
            this.blueSeekBar.setProgress(0);
        }
    }
}
