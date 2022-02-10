package com.example.myApp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class SignUpActivity extends Activity {

    EditText su_idinput;
    EditText su_passwordinput;
    EditText su_checkinput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        Button signupcomplete = (Button)findViewById(R.id.SignupComplete);
        Button signupcancel = (Button)findViewById(R.id.SignupCancel);



        signupcomplete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String su_id = su_idinput.getText().toString();
                String su_password = su_passwordinput.getText().toString();
                String su_check = su_checkinput.getText().toString();

                Intent intent = new Intent(getApplicationContext(),MainActivity.class);
                intent.putExtra("su_id",su_id);
                intent.putExtra("su_password",su_password);
                intent.putExtra("su_check",su_check);

                setResult(RESULT_OK,intent);
                finish();
            }
        });
        signupcancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });


        su_idinput = (EditText) findViewById(R.id.editTextIDSignUp);
        su_passwordinput = (EditText) findViewById(R.id.editTextPasswordSignUp);
        su_checkinput = (EditText) findViewById(R.id.editTextPasswordSignUpCheck);
    }
}
