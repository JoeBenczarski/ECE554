package com.example.light_controller;

import android.app.Activity;
import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.ListAdapter;
import android.widget.TextView;

public class ListViewArrayAdapter extends BaseAdapter
{
    Context context;
    Device[] devices = new Device[30];

    public ListViewArrayAdapter(Context context, String[] addresses, String[] devNames)
    {
        this.context  = context;
        for(int i=0;i<addresses.length;i++)
        {
            devices[i] = new Device(devNames[i], addresses[i]);
        }
    }

    @Override
    public int getCount() {
        return devices.length;
    }

    @Override
    public Object getItem(int position) {
        return devices[position];
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent)
    {

        //LayoutInflater inflater = (LayoutInflater) context.getSystemService(Activity.LAYOUT_INFLATER_SERVICE);
        //View view = inflater.inflate(R.layout.single_device_layout, null);

        if (convertView == null)
        {
            convertView = LayoutInflater.from(context).inflate(R.layout.single_device_layout, parent, false);
        }

        TextView name = (TextView) convertView.findViewById(R.id.devName);
        TextView addr = (TextView) convertView.findViewById(R.id.address);

        addr.setText(this.devices[position].address);
        name.setText(this.devices[position].name);
        return convertView;
    }
}
