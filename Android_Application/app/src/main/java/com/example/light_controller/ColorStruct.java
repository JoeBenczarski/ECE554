/*************************************************************************/
/*  File Name:  ColorStruct.java                                         */
/*  Purpose:    RGB container class.                                     */
/*  Created by: Darren Cicala on 21/03/20.                               */
/*  Copyright © 2020 Darren Cicala, Joe Benczarski, Dan Beier.           */
/*  All rights reserved.                                                 */
/*************************************************************************/

package com.example.light_controller;

public class ColorStruct
{
    int r, g, b;     // local integer RGB values (0-255)

    /* constructor, assigns default values of 0 */
    public ColorStruct()
    {
        this.r = 0;
        this.g = 0;
        this.b = 0;
    }

    /* overloaded constructor, assigns passed-in values */
    public ColorStruct(int r, int g, int b)
    {
        this.r = r;
        this.g = g;
        this.b = b;
    }

    /* updates the values in this class instance with new ones */
    public void updateColor(int r, int g, int b)
    {
        this.r = r;
        this.g = g;
        this.b = b;
    }
}
