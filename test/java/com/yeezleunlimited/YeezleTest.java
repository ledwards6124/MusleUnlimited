package com.yeezleunlimited;

import static org.junit.Assert.assertNotNull;

import org.junit.Test;

public class YeezleTest {
   
    @Test
    public void testConstructor() {
        Yeezle y = new Yeezle();
        assertNotNull(y);
    }

    @Test
    public void testAccessors() {
        Yeezle y = new Yeezle();
        assertNotNull(y.getSongMap());
        assertNotNull(y.getCurrentGuesses());
        assertNotNull(y.getMaxGuesses());
        assertNotNull(y.getSolution());
    }
}
