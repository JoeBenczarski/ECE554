/*************************************************************************/
/*  File Name:  AddColorButtonListener.java                              */
/*  Purpose:    Listener for the "add color to list" button.             */
/*  Created by: Darren Cicala on 21/03/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/

package com.example.light_controller;

/******************************* imports *********************************/
import java.util.ArrayList;
import java.util.List;

public class BluetoothMessageClass
{
    List<ColorStruct> colors;          // list of colors (ColorStruct has RGB fields)
    String lightType;                  // light type (solid, pulse, wheel)
    double frequency;                     // frequency of the light pulse (1-10 hz)
    String direction;                  // direction for the lights to travel (if shift)
    int numLEDs, numColors;            // number of LEDs and number of colors currently stored
    String stringToTransmit;           // assembled csv string to send

    /* constructor, set defaults on creation */
    public BluetoothMessageClass()
    {
        this.colors = new ArrayList<ColorStruct>();
        this.numLEDs   = 0;
        this.numColors = 0;
        this.frequency = 0;

        //ConstructCSVStr();
    }

    public void ClearMessage()
    {
        this.colors = new ArrayList<ColorStruct>();
        this.numLEDs   = 0;
        this.numColors = 0;
        this.frequency = 0;

        this.lightType = "Solid";
        this.stringToTransmit = "";
    }

    /* adds an RGB color to the list of colors */
    public void AddColor(int r, int g, int b)
    {
        ColorStruct localColor = new ColorStruct(r, g, b);
        this.colors.add(localColor);
        this.numColors++;
    }

    /* sets the light type for a given input */
    public void SetLightType(String type)
    {
        this.lightType = type;
    }

    /* sets the number of LEDs for a given input */
    public void SetNumLEDs(int num)
    {
        this.numLEDs = num;
    }

    /* sets the direction of the LEDs for a given input */
    public void SetDirection(String direction)
    {
        this.direction = direction;
    }

    /* sets the direction of the LEDs for a given input */
    public void SetFrequency(double frequency)
    {
        this.frequency = frequency;
    }

    /* builds a CSV string based on whats currently stored in this class */
    public void ConstructCSVStr()
    {
        /* first clear the old string */
        this.stringToTransmit = "";

        /* then assign the new values */
        this.stringToTransmit = this.lightType + ";" + String.valueOf(this.numLEDs) + ";" + String.valueOf(this.frequency) + ";";

        if(numColors == 0)
        {
            this.stringToTransmit += "0,0,0;";
        }
        else
        {
            /* loop over all colors, adding each RGB to the CSV string */
            for(int i =0; i < this.colors.size(); i++)
            {
                this.stringToTransmit += String.valueOf(this.colors.get(i).r) + "," + String.valueOf(this.colors.get(i).g) + "," + String.valueOf(this.colors.get(i).b) + ";";
            }
        }

        this.stringToTransmit += "\n";
    }
}
