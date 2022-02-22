package com.example.myApp.State;

import com.google.gson.annotations.SerializedName;

public class StateRequest {
    @SerializedName("id")
    private String id;

    private String state;

    public StateRequest(String id) {
        this.id = id;
    }

    public StateRequest(String id, String state) {
        this.id = id;
        this.state = state;
    }
}
