package com.yeezleunlimited;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

import org.junit.Test;

public class SongTest {
    
    @Test
    public void testConstructor() {
        Song song = new Song("Come to Life", 10, 22, Duration.ofMinutes(5).plusSeconds(10), new ArrayList<String>());
        assertNotNull(song);
    }

    @Test
    public void testAccessors() {
        Song song = new Song("Come to Life", 10, 22, Duration.ofMinutes(5).plusSeconds(10), new ArrayList<String>());
        String name = song.getName();
        int album = song.getAlbum();
        int track = song.getTrack();
        Duration length = song.getLength();
        List<String> features = song.getFeatures();
        assertEquals(name, "Come to Life");
        assertEquals(album, 10);
        assertEquals(track, 22);
        assertEquals(length, Duration.ofMinutes(5).plusSeconds(10));
        assertEquals(features, new ArrayList<String>());
    }
}
