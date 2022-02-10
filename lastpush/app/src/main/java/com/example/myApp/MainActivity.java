package com.example.myApp;

import static android.content.ContentValues.TAG;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    EditText idinput;
    EditText passwordinput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button login = (Button) findViewById(R.id.Loginbt);
        Button signup = (Button) findViewById(R.id.SignupBt);

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String id = idinput.getText().toString();
                String password = passwordinput.getText().toString();

                Intent intent = new Intent(getApplicationContext(),MenuActivity.class);
                intent.putExtra("id",id);
                intent.putExtra("password",password);
                Log.i(TAG,"id: " + id);
                Log.i(TAG,"password: " + password);

                startActivity(intent);

            }
        });

        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, SignUpActivity.class);
                startActivityForResult(intent,0);
            }
        });

        idinput = (EditText) findViewById(R.id.editTextID);
        passwordinput = (EditText) findViewById(R.id.editTextPassword);



    }


}