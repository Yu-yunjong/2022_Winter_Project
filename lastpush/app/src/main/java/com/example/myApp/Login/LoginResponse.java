package com.example.myApp.Login;

import com.google.gson.annotations.SerializedName;

public class LoginResponse {

    @SerializedName("code")
    public String code;


    @SerializedName("reason")
    public String reason;

    public String getCode() {
        return code;
    }

    public void setResultCode(String code) {
        this.code = code;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }
}