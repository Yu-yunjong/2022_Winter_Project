package com.example.myApp.Signup;

import com.google.gson.annotations.SerializedName;

public class SignupRequest {
    @SerializedName("id")
    private String id;

    @SerializedName("pwd")
    private String pwd;

    @SerializedName("server")
    private String server;

    public SignupRequest(String id, String pwd, String server) {
        this.id = id;
        this.pwd = pwd;
        this.server = server;
    }
}
