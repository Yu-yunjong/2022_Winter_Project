package com.example.myApp.Activity;

import android.app.Activity;
import android.graphics.Rect;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;

import com.example.myApp.R;
import com.example.myApp.Service.RetrofitClient;
import com.example.myApp.Signup.SignupRequest;
import com.example.myApp.Signup.SignupResponse;
import com.example.myApp.Service.initMyApi;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignUpActivity extends Activity {

    EditText su_idinput;
    EditText su_pwinput;
    EditText su_checkinput;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        su_idinput = (EditText) findViewById(R.id.editTextIDSignUp);
        su_pwinput = (EditText) findViewById(R.id.editTextPasswordSignUp);
        su_checkinput = (EditText) findViewById(R.id.editTextPasswordSignUpCheck);

        Button signupcomplete = (Button) findViewById(R.id.SignupComplete);
        Button signupcancel = (Button) findViewById(R.id.SignupCancel);


        signupcomplete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String su_id = su_idinput.getText().toString();
                String su_pw = su_pwinput.getText().toString();
                String su_check = su_checkinput.getText().toString();

                //로그인 정보 미입력 시
                if (su_id.trim().length() == 0 || su_pw.trim().length() == 0 || su_id == null || su_pw == null) {

                    AlertDialog.Builder builder = new AlertDialog.Builder(SignUpActivity.this);
                    builder.setTitle("알림")
                            .setMessage("회원가입 정보를 입력바랍니다.")
                            .setPositiveButton("확인", null)
                            .create()
                            .show();
                    AlertDialog alertDialog = builder.create();
                    alertDialog.show();

                } else if (!su_pw.trim().equals(su_check.trim())) {

                    AlertDialog.Builder builder = new AlertDialog.Builder(SignUpActivity.this);
                    builder.setTitle("알림")
                            .setMessage("비밀번호가 일치하지 않습니다..")
                            .setPositiveButton("확인", null)
                            .create()
                            .show();
                    AlertDialog alertDialog = builder.create();
                    alertDialog.show();

                } else {
                    //로그인 통신
                    SignupResponse();
                }

            }
        });
        signupcancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

    }

    private void SignupResponse() {
        su_idinput.setError(null);
        su_pwinput.setError(null);

        Spinner server_sel = (Spinner) findViewById(R.id.server);

        String id = su_idinput.getText().toString().trim();
        String pwd = su_pwinput.getText().toString().trim();
        String server = server_sel.getSelectedItem().toString();

        SignupRequest signupRequest = new SignupRequest(id,pwd,server);

        boolean cancel = false;
        View focusView = null;


        if (!isEmailValid(id)) {
            su_idinput.setError("@를 포함한 유효한 이메일을 입력해주세요.");
            focusView = su_idinput;
            cancel = true;
        }

        if (cancel) {
            focusView.requestFocus();
        } else {
            startSignup(new SignupRequest( id , pwd, server));
        }
    }

    private void startSignup(SignupRequest data) {


        RetrofitClient retrofitClient = RetrofitClient.getInstance();
        initMyApi initMyApi = RetrofitClient.getRetrofitInterface();


        initMyApi.userSignup(data).enqueue(new Callback<SignupResponse>() {
            @Override
            public void onResponse(Call<SignupResponse> call, Response<SignupResponse> response) {

                String resultcode = String.valueOf(response.code());
                Log.d("result http: ",resultcode);

                if (resultcode.equals("200")) {
                    Log.d("success 200 http: ",resultcode);
                    Toast.makeText(SignUpActivity.this, "회원가입 성공", Toast.LENGTH_SHORT).show();
                    finish();
                }
                else if (resultcode.equals("300")) {
                    Log.d("error 300 http: ",resultcode);

                    Toast.makeText(SignUpActivity.this, "이미 존재하는 아이디 입니다.", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<SignupResponse> call, Throwable t) {
                Toast.makeText(SignUpActivity.this, "회원가입 에러 발생", Toast.LENGTH_SHORT).show();
                Log.e("회원가입 에러 발생", t.getMessage());
            }
        });
    }

    private boolean isEmailValid(String email) {
        return email.contains("@");
    }

    //화면 터치 시 키보드 내려감
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
