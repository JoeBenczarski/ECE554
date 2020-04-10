package com.example.light_controller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class ConnectionsActivity extends AppCompatActivity {

    ListView connectionsList;
    ListAdapter adapter;
    Intent intent;
    Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connections);

        connectionsList = (ListView) findViewById(R.id.bluetoothConnections);

        this.context = getApplicationContext();

        intent = getIntent();
        final String[] addresses = intent.getStringArrayExtra("addresses");
        final String[] names     = intent.getStringArrayExtra("names");

        adapter = new ListViewArrayAdapter(this.getApplicationContext(), addresses, names);
        connectionsList.setAdapter(adapter);
        connectionsList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                // dont click on something illegal
                if(position > addresses.length)
                {
                    Toast.makeText(context, "Incorrect device selected!", Toast.LENGTH_LONG).show();
                }
                else
                {
                    intent.putExtra("deviceID", position);
                    setResult(0,intent);
                    finish();
                }
            }
        });
    }
}
