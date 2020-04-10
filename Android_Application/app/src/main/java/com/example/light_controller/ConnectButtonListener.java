package com.example.light_controller;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class ConnectButtonListener implements Button.OnClickListener
{

    Context context;
    Activity activity;
    private static final int SECOND_ACTIVITY_REQUEST_CODE = 0;

    public ConnectButtonListener(Context context, Activity activity)
    {
        this.context = context;
        this.activity = activity;
    }

    @Override
    public void onClick(View v)
    {
        String[] deviceNames = new String[30];
        String[] macAddrs    = new String[30];
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter != null)
        { // there is a bluetooth adapter on this device

            if (blueAdapter.isEnabled())
            { // the bluetooth adapter is enabled

                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();
                if(bondedDevices.size() > 0)
                { // there are some bonded devices to this phone
                    List<BluetoothDevice> devices = new ArrayList<>(bondedDevices); //(BluetoothDevice[]) bondedDevices.toArray();  // cast this list to an indexable array
                    for(int i = 0; i < devices.size(); i++)
                    {
                        deviceNames[i] = devices.get(i).getName();
                        macAddrs[i]    = devices.get(i).getAddress();
                    }
                    Intent intent = new Intent(context, ConnectionsActivity.class);
                    intent.putExtra("names", deviceNames);
                    intent.putExtra("addresses", macAddrs);
                    activity.startActivityForResult(intent, SECOND_ACTIVITY_REQUEST_CODE);
                }
                else
                {
                    Toast.makeText(context, "No paired Bluetooth devices!", Toast.LENGTH_LONG).show();
                }
            }
            else
            {
                Toast.makeText(context, "Bluetooth not currently enabled on this device!", Toast.LENGTH_LONG).show();
            }
        }
        else
        {
            Toast.makeText(context, "Bluetooth not supported on this device!", Toast.LENGTH_LONG).show();
        }
    }
}
