package com.example.myApp.Signup;

import com.google.gson.annotations.SerializedName;

public class SignupResponse {
    @SerializedName("code")
    public String code;

    @SerializedName("reason")
    public String reason;

    public String getCode() {
        return code;
    }

    public String getReason() {
        return reason;
    }
}
