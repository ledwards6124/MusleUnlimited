package com.yeezleunlimited;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public class Yeezle {
    
    private Song solution;
    private int maxGuesses;
    private int currGuesses;
    private HashMap<String, Song> songMap;
    private Song[] prevGuesses;
    private int prevIndex;

    public Yeezle() {
        this.currGuesses = 0;
        this.maxGuesses = 8;
        this.songMap = Parser.generateSongMap();
        Random r = new Random();
        int randomIndex = songMap.size() > 0 ? r.nextInt(songMap.size()) : 0;
        this.solution = Parser.parseFile().get(randomIndex);
        this.prevGuesses = new Song[8];
        this.prevIndex = 0;
    }

    public Song getSolution() {
        return this.solution;
    }

    public int getMaxGuesses() {
        return this.maxGuesses;
    }

    public int getCurrentGuesses() {
        return this.currGuesses;
    }

    public HashMap<String, Song> getSongMap() {
        return this.songMap;
    }

    public int[] guess(Song song) {
        this.currGuesses ++;
        prevGuesses[prevIndex] = song;
        prevIndex ++;
        int[] matches = new int[4];
        matches[0] = scoreAlbum(song);
        matches[1] = scoreTrack(song);
        matches[2] = scoreLength(song);
        matches[3] = scoreFeatures(song);
        return matches;
    }

    private int scoreAlbum(Song song) {
        int tracker = 0;
        ArrayList<Integer> range = new ArrayList<>();
        int solutionTrack = this.solution.getAlbum();
        range.add(0, solutionTrack - 2);
        range.add(1, solutionTrack - 1);
        range.add(2, solutionTrack + 1);
        range.add(3, solutionTrack + 2);
        if (song.getAlbum() == solutionTrack) {
            tracker = 2;
            return tracker;
        } else if (range.contains(song.getAlbum())) {
            tracker = 1;
            if (this.solution.getAlbum() < song.getAlbum()) {
                tracker *= -1;
            }
            return tracker;
        }
        return tracker;
    }

    private int scoreTrack(Song song) {
        int tracker = 0;
        ArrayList<Integer> range = new ArrayList<>();
        int solutionTrack = this.solution.getTrack();
        range.add(0, solutionTrack - 2);
        range.add(1, solutionTrack - 1);
        range.add(2, solutionTrack + 1);
        range.add(3, solutionTrack + 2);
        if (song.getTrack() == solutionTrack) {
            tracker = 2;
            return tracker;
        } else if (range.contains(song.getTrack())) {
            tracker = 1;
            if (this.solution.getTrack() < song.getTrack()) {
                tracker *= -1;
            }
            return tracker;
        }
        return tracker;
    }

    private int scoreFeatures(Song song) {
        int tracker = 0;
        if (song.getFeatures().equals(this.solution.getFeatures())) {
            tracker = 2;
            return tracker;
        }
        for (String s : song.getFeatures()) {
            if (this.solution.getFeatures().contains(s)) {
                tracker = 1;
            }   
        }
        return tracker;
    }

    public boolean gameIsOver() {
        return this.currGuesses > this.maxGuesses;
    }

    public boolean gameIsWon(int[] scores) {
        for (Integer i : scores) {
            if (i != 2) {
                return false;
            }
        }
        return true;
    }

    public void printGame() {
        System.out.println("Previous Guesses: ");
        System.out.println(this.currGuesses + "/" + this.maxGuesses + " Guesses Used");
        System.out.println("Name | Album | Track | Duration | Features");
        for (Song s : prevGuesses) {
            if (s == null) {
                continue;
            } else {
                System.out.println(s.getName() + " | " + s.getAlbum() + " | " + 
                s.getTrack() + " | " + s.getLength() + " | " + s.getFeatures());
            }
        }
    }


    private int scoreLength(Song song) {
        long songSeconds = song.getLength().getSeconds();
        long solutionSeconds = this.solution.getLength().getSeconds();
        long difference = songSeconds - solutionSeconds;
        if (difference == 0) {
            return 2;
        } else if (difference < 0 && Math.abs(difference) <= 30) {
            return -1;
        } else if (difference > 0 && Math.abs(difference) <= 30) {
            return 1;
        }
        return 0;
    }
    
    

    public static void main(String[] args) {
        Yeezle yeezle = new Yeezle();
        Song s = new Song("Come to Life", 11, 4, Duration.ofMinutes(3).plusSeconds(10), new ArrayList<String>());
        System.out.println(yeezle.getSolution());
        int[] guess = yeezle.guess(s);
        for (Integer i : guess) {
            System.out.println(i);
        }
    }
}
