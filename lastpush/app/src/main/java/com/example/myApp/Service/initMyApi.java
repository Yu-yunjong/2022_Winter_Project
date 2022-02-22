package com.example.myApp.Service;

import com.example.myApp.Keyword.KeywordRequest;
import com.example.myApp.Keyword.KeywordResponse;
import com.example.myApp.Login.LoginRequest;
import com.example.myApp.Login.LoginResponse;
import com.example.myApp.Signup.SignupRequest;
import com.example.myApp.Signup.SignupResponse;
import com.example.myApp.State.StateRequest;
import com.example.myApp.State.StateResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface initMyApi {
    //@통신 방식("통신 API명")
    //@Headers({"Content-Type:application/x-www-form-urlencoded","Host:https://weidb.franky.tk"})
    @POST("/loginCheck")
    Call<LoginResponse> getLoginResponse(@Body LoginRequest loginRequest);

    //@Headers({"Content-Type:application/x-www-form-urlencoded","Host:https://weidb.franky.tk"})
    @POST("/addUserDB")
    Call<SignupResponse> userSignup(@Body SignupRequest data);

    @POST("/insertKeyword")
    Call<KeywordResponse> setKeyword(@Body KeywordRequest data);

    @POST("/updateCrawllingState")
    Call<StateResponse> stateResponse(@Body StateRequest data);
}