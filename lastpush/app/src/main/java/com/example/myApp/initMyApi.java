package com.example.myApp;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface initMyApi {
    //@통신 방식("통신 API명")
    //@Headers({"Content-Type:application/x-www-form-urlencoded","Host:https://weidb.franky.tk"})
    @POST("/addUserDB")
    Call<LoginResponse> getLoginResponse(@Body LoginRequest loginRequest);

    //@Headers({"Content-Type:application/x-www-form-urlencoded","Host:https://weidb.franky.tk"})
    @POST("/addUserDB")
    Call<SignupResponse> userSignup(@Body SignupRequest data);
}