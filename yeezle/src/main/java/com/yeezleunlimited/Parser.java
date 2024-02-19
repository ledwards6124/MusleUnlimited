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
    public static HashMap<Integer, String> albums = new HashMap<>();

    static {
        albums.put(1, "The College Dropout");
        albums.put(2, "Late Registration");
        albums.put(3, "Graduation");
        albums.put(4, "808's & Heartbreaks");
        albums.put(5, "My Beautiful Dark Twisted Fantasy");
        albums.put(6, "Watch The Throne");
        albums.put(7, "Yeezus");
        albums.put(8, "The Life of Pablo");
        albums.put(9, "Ye");
        albums.put(10, "Kids See Ghosts");
        albums.put(11, "Jesus Is King");
        albums.put(12, "Donda");
        albums.put(13, "VULTURES 1");
    }
    
    public static String albumNumToName(int albumNum) {
        return albums.containsKey(albumNum) ? albums.get(albumNum) : "Invalid album number";
    }

    public static String durationToString(Duration d) {
        String duration = "";
        int seconds = (int)d.getSeconds();
        int minutes = Math.floorDiv(seconds, 60);
        int remainingSeconds = seconds - (minutes * 60);
        String oString = "0";
        if (remainingSeconds < 10) {
            duration += Integer.toString(minutes) + ":" + oString + Integer.toString(remainingSeconds);
        } else {
            duration += Integer.toString(minutes) + ":" + Integer.toString(remainingSeconds);
        }
        
        return duration;
    }
    
    public static ArrayList<String> parseFeatures(String features) {
        features = features.substring(1, features.length() - 1);
        if (features.length() == 0) {
            return new ArrayList<>();
        } else {
            String[]splitFeatrues = features.split("-");
            return new ArrayList<>(Arrays.asList(splitFeatrues));
        }   
    }

    public static Duration parseLength(String length) {
        String[]values = length.split(":");
        int minutes = Integer.parseInt(values[0].replace(" ", ""));
        int seconds = Integer.parseInt(values[1].replace(" ", ""));
        return Duration.ofMinutes(minutes).plusSeconds(seconds);
    }

    public static ArrayList<Song> parseFile() {
        ArrayList<Song> songList = new ArrayList<>();
        try (BufferedReader bReader = new BufferedReader(new FileReader(FILEPATH))) {
            String line;
            int tracker = 0;
            while ((line = bReader.readLine()) != null) {
                if (tracker == 0 || line.equals("###")) {
                    tracker = 1;
                    continue;
                }
                String[]values = line.split(",");
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
                songMap.put(s.getName().toUpperCase(), s);
            }
        }
        return songMap;
    }

    public static HashMap<String, Song> generateSongMap() {
        ArrayList<Song> songs = parseFile();
        return mapNameToSong(songs);
    }
}
