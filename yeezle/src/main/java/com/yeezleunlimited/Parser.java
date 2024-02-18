package com.yeezleunlimited;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Parser {

    public static String FILEPATH = "yeezle\\data\\discography.csv";
    
    public static ArrayList<String> parseFeatures(String features) {
        if (features.length() == 2) {
            return new ArrayList<>();
        } else {
            features = features.substring(1, features.length() - 1);
            String[] splitFeatrues = features.split("-");
            return new ArrayList<>(Arrays.asList(splitFeatrues));
        }   
    }

    public static Duration parseLength(String length) {
        String[] values = length.split(":");
        int minutes = Integer.parseInt(values[0].replace(" ", ""));
        int seconds = Integer.parseInt(values[1].replace(" ", ""));
        return Duration.ofMinutes(minutes).plusSeconds(seconds);
    }

    public static ArrayList<Song> parseFile(String path) {
        ArrayList<Song> songList = new ArrayList<>();
        try (BufferedReader bReader = new BufferedReader(new FileReader(path))) {
            String line;
            int tracker = 0;
            while ((line = bReader.readLine()) != null) {
                if (tracker == 0 || line.equals("###")) {
                    tracker = 1;
                    continue;
                }
                String[] values = line.split(",");
                String name = values[0];
                int album = Integer.parseInt(values[1].replace(" ", ""));
                int track = Integer.parseInt(values[2].replace(" ", ""));
                Duration length = parseLength(values[3]);
                ArrayList<String> featues = parseFeatures(values[4]);
                Song song = new Song(name, album, track, length, featues);
                songList.add(song);
            }
        } catch (IOException e) {
            System.out.println("Error reading file... Please try again...");
        }
        return songList;
    }

    public static HashMap<String, Song> mapNameToSong(ArrayList<Song> songs) {
        HashMap<String, Song> songMap = new HashMap<>();
        for (Song s : songs) {
            if (!songMap.containsKey(s.getName())) {
                songMap.put(s.getName(), s);
            }
        }
        return songMap;
    }

    public static HashMap<String, Song> generateSongMap() {
        ArrayList<Song> songs = parseFile(FILEPATH);
        return mapNameToSong(songs);
    }

    public static void main(String[] args) {
        ArrayList<Song> songs = parseFile("yeezle\\data\\discography.csv");
        HashMap<String, Song> songMap = mapNameToSong(songs);
        for (String s : songMap.keySet()) {
            System.out.println(songMap.get(s));
        }
    }
}
