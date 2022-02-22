package com.example.myApp.Activity;

import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.myApp.Keyword.KeywordRequest;
import com.example.myApp.Keyword.KeywordResponse;
import com.example.myApp.Service.PreferenceManager;
import com.example.myApp.R;
import com.example.myApp.Service.RetrofitClient;
import com.example.myApp.Service.initMyApi;
import com.example.myApp.Signup.SignupRequest;
import com.example.myApp.Signup.SignupResponse;
import com.example.myApp.State.StateRequest;
import com.example.myApp.State.StateResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MenuActivity extends AppCompatActivity {
    Switch onoff;
    private Context mContext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        mContext = this;

        CheckStateResponse();

        Button save = (Button)findViewById(R.id.save);
        Button logout = (Button)findViewById(R.id.logoutbt);
        onoff = (Switch)findViewById(R.id.onoff);

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                keywordResponse();
            }
        });

        onoff.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if(onoff.isChecked()){
                    StateResponse();
                    Toast.makeText(MenuActivity.this, "알림이 켜졌습니다.", Toast.LENGTH_SHORT).show();
                }else{
                    StateResponse();
                    Toast.makeText(MenuActivity.this, "알림이 꺼졌습니다.", Toast.LENGTH_SHORT).show();
                }
            }
        });


        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                PreferenceManager.setString(mContext,"id","");
                finish();
            }
        });
    }

    private void keywordResponse() {

        Spinner keyword = (Spinner) findViewById(R.id.keyword);

        String id = PreferenceManager.getString(mContext,"id");
        String keyword_sel = keyword.getSelectedItem().toString();

        KeywordRequest keywordRequest = new KeywordRequest(id,keyword_sel);


        startKeyword(new KeywordRequest(id,keyword_sel));

    }

    private void startKeyword(KeywordRequest data) {


        RetrofitClient retrofitClient = RetrofitClient.getInstance();
        initMyApi initMyApi = RetrofitClient.getRetrofitInterface();


        initMyApi.setKeyword(data).enqueue(new Callback<KeywordResponse>() {
            @Override
            public void onResponse(Call<KeywordResponse> call, Response<KeywordResponse> response) {
                KeywordResponse result = response.body();

                String resultcode = String.valueOf(response.code());
                Log.d("result http: ",resultcode);

                if (resultcode.equals("200")) {
                    Log.d("success 200 http: ",resultcode);
                    Toast.makeText(MenuActivity.this, "저장되었습니다.", Toast.LENGTH_SHORT).show();
                }
                else if (resultcode.equals("300")) {
                    Log.d("error 300 http: ",resultcode);
                    Toast.makeText(MenuActivity.this, "저장에 실패했습니다.", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<KeywordResponse> call, Throwable t) {
                Toast.makeText(MenuActivity.this, "알 수 없는 에러 발생", Toast.LENGTH_SHORT).show();
                Log.e("알 수 없는 에러 발생", t.getMessage());
            }
        });
    }

    private void CheckStateResponse() {

        String id = PreferenceManager.getString(mContext,"id");

        checkState(new StateRequest(id));

    }

    private void checkState(StateRequest data) {
        onoff = (Switch) findViewById(R.id.onoff);


        RetrofitClient retrofitClient = RetrofitClient.getInstance();
        initMyApi initMyApi = RetrofitClient.getRetrofitInterface();


        initMyApi.stateResponse(data).enqueue(new Callback<StateResponse>() {
            @Override
            public void onResponse(Call<StateResponse> call, Response<StateResponse> response) {
                StateResponse result = response.body();

                String resultcode = String.valueOf(result.getCode());
                String resultstate = String.valueOf(result.getState());
                Log.d("result http: ",resultcode);

                if (resultcode.equals("200")) {
                    Log.d("success 200 http: ",resultcode);

                    if(resultstate.equals("True")){
                        onoff.setChecked(true);
                    } else if(resultstate.equals("False")){
                        onoff.setChecked(false);
                    }
                }
                else if (resultcode.equals("300")) {
                    Log.d("error 300 http: ",resultcode);
                }
            }

            @Override
            public void onFailure(Call<StateResponse> call, Throwable t) {
                Toast.makeText(MenuActivity.this, "알 수 없는 에러 발생", Toast.LENGTH_SHORT).show();
                Log.e("알 수 없는 에러 발생", t.getMessage());
            }
        });
    }

    private void StateResponse() {

        onoff = (Switch) findViewById(R.id.onoff);

        String id = PreferenceManager.getString(mContext,"id");
        String state;

        if(onoff.isChecked()){
            state = "True";
        } else{
            state = "False";
        }

        StateChange(new StateRequest(id,state));

    }

    private void StateChange(StateRequest data) {
        onoff = (Switch) findViewById(R.id.onoff);


        RetrofitClient retrofitClient = RetrofitClient.getInstance();
        initMyApi initMyApi = RetrofitClient.getRetrofitInterface();


        initMyApi.stateResponse(data).enqueue(new Callback<StateResponse>() {
            @Override
            public void onResponse(Call<StateResponse> call, Response<StateResponse> response) {
                StateResponse result = response.body();

                String resultcode = String.valueOf(response.code());
                Log.d("result http: ",resultcode);

                if (resultcode.equals("200")) {
                    Log.d("success 200 http: ",resultcode);

                }
                else if (resultcode.equals("300")) {
                    Log.d("error 300 http: ",resultcode);
                }
            }

            @Override
            public void onFailure(Call<StateResponse> call, Throwable t) {
                Toast.makeText(MenuActivity.this, "알 수 없는 에러 발생", Toast.LENGTH_SHORT).show();
                Log.e("알 수 없는 에러 발생", t.getMessage());
            }
        });
    }

}
