package com.example.myApp.State;

import com.google.gson.annotations.SerializedName;

public class StateResponse {
    @SerializedName("code")
    private String code;

    @SerializedName("reason")
    private String reason;

    @SerializedName("state")
    private String state;

    public String getCode() {
        return code;
    }

    public String getReason() {
        return reason;
    }

    public String getState() { return  state; }
}
