package com.example.myApp.Login;

import com.google.gson.annotations.SerializedName;

public class LoginRequest {

    @SerializedName("id")
    public String id;

    @SerializedName("pwd")
    public String pwd;

    @SerializedName("appnum")
    public String appnum;

    public String getInputId() {
        return id;
    }

    public String getInputPw() {
        return pwd;
    }

    public String getAppnum() {
        return appnum;
    }

    public void setInputId(String id) {
        this.id = id;
    }

    public void setInputPw(String pwd) {
        this.pwd = pwd;
    }

    public void setAppnum(String appnum) {
        this.appnum = appnum;
    }

    public LoginRequest(String id, String pwd, String appnum) {
        this.id = id;
        this.pwd = pwd;
        this.appnum = appnum;
    }
}