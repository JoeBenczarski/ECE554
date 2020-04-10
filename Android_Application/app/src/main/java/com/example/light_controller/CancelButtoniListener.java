/*************************************************************************/
/*  File Name:  CancelButtoniListener.java                               */
/*  Purpose:    Routine to perform when the user presses cancel.         */
/*  Created by: Darren Cicala on 05/04/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/

package com.example.light_controller;

import android.graphics.Color;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Spinner;

public class CancelButtoniListener implements View.OnClickListener
{
    SeekBar redSlider, greenSlider, blueSlider;
    Spinner lightType, frequency, numLEDs;
    Button color1, color2, color3, color4;
    BluetoothMessageClass bluetoothMessage;

    /* class constructor */
    public CancelButtoniListener(SeekBar redSlider, SeekBar greenSlider, SeekBar blueSlider, Spinner lightType, Spinner frequency, Spinner numLEDs, Button[] buttonList, BluetoothMessageClass bluetoothMessage)
    {
        this.redSlider   = redSlider;
        this.greenSlider = greenSlider;
        this.blueSlider  = blueSlider;
        this.lightType   = lightType;
        this.frequency   = frequency;
        this.numLEDs     = numLEDs;
        this.color1      = buttonList[0];
        this.color2      = buttonList[1];
        this.color3      = buttonList[2];
        this.color4      = buttonList[3];

        this.bluetoothMessage = bluetoothMessage;
    }

    @Override
    public void onClick(View v)
    {
        this.bluetoothMessage.ClearMessage();

        this.redSlider.setProgress(0);
        this.greenSlider.setProgress(0);
        this.blueSlider.setProgress(0);

        this.lightType.setSelection(0);
        this.frequency.setSelection(0);
        this.numLEDs.setSelection(0);

        this.color1.setBackgroundColor(Color.rgb(211,211,211));
        this.color2.setBackgroundColor(Color.rgb(211,211,211));
        this.color3.setBackgroundColor(Color.rgb(211,211,211));
        this.color4.setBackgroundColor(Color.rgb(211,211,211));
    }
}
