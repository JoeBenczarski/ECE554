/*************************************************************************/
/*  File Name:  SeekBarListener.java                                     */
/*  Purpose:    Listener for the different seekbars.                     */
/*  Created by: Darren Cicala on 21/03/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/

package com.example.light_controller;

/******************************* imports *********************************/
import android.graphics.Color;
import android.widget.Button;
import android.widget.SeekBar;

public class SeekBarListener implements SeekBar.OnSeekBarChangeListener
{

    Button  addColorButton;                          // this button gets its color changed whenever any of the sliders are changed
    SeekBar redSeekBar, greenSeekBar, blueSeekBar;   // local references of the sliders to get their progress

    /* constructor. creates local references of the passed in variables */
    public SeekBarListener(Button addColorButton, SeekBar redSeekBar, SeekBar greenSeekBar, SeekBar blueSeekBar)
    {
        this.addColorButton = addColorButton;
        this.redSeekBar     = redSeekBar;
        this.greenSeekBar   = greenSeekBar;
        this.blueSeekBar    = blueSeekBar;
    }

    /* this gets called whenever the progress is changed on any of the three seekbars */
    @Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser)
    {
        /* set the background color to the selected RGB color */
        this.addColorButton.setBackgroundColor(Color.rgb(this.redSeekBar.getProgress(), this.greenSeekBar.getProgress(), this.blueSeekBar.getProgress()));

        /* should probably tune this later, but text should be white when sufficiently dark, and black when sufficiently light */
        if(this.redSeekBar.getProgress() < 100 || this.greenSeekBar.getProgress() < 100 || this.blueSeekBar.getProgress() < 100)
        {
            this.addColorButton.setTextColor(Color.rgb(255,255,255)); // white text
        }
        else
        {
            this.addColorButton.setTextColor(Color.rgb(0,0,0));  // black text
        }
    }

    /* don't care about these, ignore them */
    @Override
    public void onStartTrackingTouch(SeekBar seekBar)
    {

    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar)
    {

    }
}
