package com.example.myApp;

import com.google.gson.annotations.SerializedName;

public class SignupRequest {
    @SerializedName("id")
    private String id;

    @SerializedName("pwd")
    private String pwd;

    public SignupRequest(String id, String pwd) {
        this.id = id;
        this.pwd = pwd;
    }
}
