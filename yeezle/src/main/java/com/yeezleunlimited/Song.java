package com.yeezleunlimited;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

public class Song {
    
    private String name;
    private int album;
    private int track;
    private Duration length;
    private ArrayList<String> features;

    public Song(String name, int album, int track, Duration length, ArrayList<String> features) {
        this.name = name;
        this.album = album;
        this.track = track;
        this.length = length;
        this.features = features;
    }

    public String getName() {
        return this.name;
    }

    public int getAlbum() {
        return this.album;
    }

    public int getTrack() {
        return this.track;
    }

    public Duration getLength() {
        return this.length;
    }

    public List<String> getFeatures() {
        return this.features;
    }

    @Override
    public String toString() {
        return "Name: " + this.name + 
        "\nAlbum: " + this.album + 
        "\nTrack: " + this.track +
        "\nLength: " + this.length + 
        "\nFeatures: " + this.features.toString();
    }
}
