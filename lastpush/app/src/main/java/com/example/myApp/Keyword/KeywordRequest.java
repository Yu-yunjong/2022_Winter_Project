package com.example.myApp.Keyword;

import com.google.gson.annotations.SerializedName;

public class KeywordRequest {
    @SerializedName("id")
    private String id;

    @SerializedName("keyword")
    private String keyword;

    public KeywordRequest(String id, String keyword) {
        this.id = id;
        this.keyword = keyword;
    }
}
