package com.example.myApp.Keyword;

import com.google.gson.annotations.SerializedName;

public class KeywordResponse {
    @SerializedName("code")
    private String code;

    @SerializedName("reason")
    private String reason;

    public String getCode() {
        return code;
    }

    public String getReason() {
        return reason;
    }
}
