package com.example.myApp.Activity;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Rect;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.myApp.Login.LoginRequest;
import com.example.myApp.Login.LoginResponse;
import com.example.myApp.Service.PreferenceManager;
import com.example.myApp.R;
import com.example.myApp.Service.RetrofitClient;
import com.example.myApp.Service.initMyApi;
import com.google.firebase.iid.FirebaseInstanceId;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    EditText idinput;
    EditText pwinput;

    String appnum = FirebaseInstanceId.getInstance().getToken();

    private Context mContext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mContext = this;

        idinput = (EditText) findViewById(R.id.editTextID);
        pwinput = (EditText) findViewById(R.id.editTextPassword);

        Button login = (Button) findViewById(R.id.Loginbt);
        Button signup = (Button) findViewById(R.id.SignupBt);

        Log.d("appnum: ",appnum);

        String autoID = PreferenceManager.getString(mContext,"id");
        String autoPassword = PreferenceManager.getString(mContext,"pwd");


        if(!autoID.equals("")){
            idinput.setText(autoID);
            pwinput.setText(autoPassword);
            LoginResponse();
        } else{
            Log.d("mContext autoID: ",autoID);
            Log.d("mContext autoPassword: ",autoPassword);
        }

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {


                String id = idinput.getText().toString();
                String pw = pwinput.getText().toString();
                hideKeyboard();

                //????????? ?????? ????????? ???
                if (id.trim().length() == 0 || pw.trim().length() == 0 || id == null || pw == null) {

                    AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                    builder.setTitle("??????")
                            .setMessage("????????? ????????? ??????????????????.")
                            .setPositiveButton("??????", null)
                            .create()
                            .show();
                    AlertDialog alertDialog = builder.create();
                    alertDialog.show();

                } else {
                    //????????? ??????
                    PreferenceManager.setString(mContext,"id",id);
                    PreferenceManager.setString(mContext,"pwd",pw);
                    LoginResponse();
                }

            }
        });

        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, SignUpActivity.class);
                startActivityForResult(intent,0);
            }
        });


    }

    public void LoginResponse() {
        String userID = idinput.getText().toString().trim();
        String userPassword = pwinput.getText().toString().trim();

        //loginRequest??? ???????????? ????????? id??? pw??? ??????
        LoginRequest loginRequest = new LoginRequest(userID, userPassword,appnum);

        //retrofit ??????
        RetrofitClient retrofitClient = RetrofitClient.getInstance();
        initMyApi initMyApi = RetrofitClient.getRetrofitInterface();

        //loginRequest??? ????????? ???????????? ?????? init?????? ????????? getLoginResponse ????????? ????????? ??? ????????? ??????
        initMyApi.getLoginResponse(loginRequest).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {

                Log.d("retrofit", "Data fetch success");

                String resultCode = String.valueOf(response.code());
                Log.d("result http: ",resultCode);


                String success = "200"; //????????? ??????
                String fail = "300"; //????????? ??????


                if (resultCode.equals(success)) {
                    String userID = idinput.getText().toString();
                    String userPassword = pwinput.getText().toString();

                    Toast.makeText(MainActivity.this, userID + "??? ???????????????.", Toast.LENGTH_LONG).show();
                    Intent intent = new Intent(MainActivity.this, MenuActivity.class);
                    intent.putExtra("userId", userID);
                    startActivity(intent);

                } else if (resultCode.equals(fail)) {

                    AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                    builder.setTitle("??????")
                            .setMessage("????????? ?????? ??????????????? ??????????????????.")
                            .setPositiveButton("??????", null)
                            .create()
                            .show();
                    AlertDialog alertDialog = builder.create();
                    alertDialog.show();

                } else {

                    AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                    builder.setTitle("??????")
                            .setMessage("????????? ?????? ????????? ?????????????????????.")
                            .setPositiveButton("??????", null)
                            .create()
                            .show();
                }
            }

            //?????? ??????
            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("??????")
                        .setMessage("????????? ?????? ????????? ?????????????????????.")
                        .setPositiveButton("??????", null)
                        .create()
                        .show();
            }
        });
    }

    //???????????? ?????? ???????????? ????????????
    public void setPreference(String key, String value){
        SharedPreferences pref = getSharedPreferences("DATA_STORE", MODE_PRIVATE);
        SharedPreferences.Editor editor = pref.edit();
        editor.putString(key, value);
        editor.apply();
    }

    //?????? ???????????? ????????? ????????? ????????????
    public String getPreferenceString(String key) {
        SharedPreferences pref = getSharedPreferences("DATA_STORE", MODE_PRIVATE);
        return pref.getString(key, "");
    }


    //????????? ?????????
    private void hideKeyboard()
    {
        InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(idinput.getWindowToken(), 0);
        imm.hideSoftInputFromWindow(pwinput.getWindowToken(), 0);
    }

    //?????? ?????? ??? ????????? ?????????
    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        View focusView = getCurrentFocus();
        if (focusView != null) {
            Rect rect = new Rect();
            focusView.getGlobalVisibleRect(rect);
            int x = (int) ev.getX(), y = (int) ev.getY();
            if (!rect.contains(x, y)) {
                InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
                if (imm != null)
                    imm.hideSoftInputFromWindow(focusView.getWindowToken(), 0);
                focusView.clearFocus();
            }
        }
        return super.dispatchTouchEvent(ev);
    }


}
