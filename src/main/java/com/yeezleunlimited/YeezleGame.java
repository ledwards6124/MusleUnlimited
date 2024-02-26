package com.yeezleunlimited;

import java.util.Scanner;

public class YeezleGame {
    
    public static void mainLoop() {
        Yeezle yeezle = new Yeezle();
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the Yeezle Unlimited CLI! Enter your favorite Kanye song!");
        try {
            while (!yeezle.gameIsOver()) {
                System.out.println("\n\n");
                yeezle.printGame();
                System.out.println("Your Guess: ");
                String guess = scanner.nextLine().toUpperCase();
                Song guessSong = yeezle.getSongMap().get(guess);
                if (guessSong != null) {
                    int[]score = yeezle.guess(guessSong);
                    String[]stringScores = new String[4];
                    for (int i = 0; i < score.length; i ++) {
                        if (score[i]== 2) {
                            stringScores[i]= "X";
                        } else if (score[i]== 1) {
                            stringScores[i]= "/\\";
                        } else if (score[i]== -1) {
                            stringScores[i]= "V";
                        } else {
                            stringScores[i]= "O";
                        }
                    }
                    if (yeezle.gameIsWon(score)) {
                        System.out.println("Album | Track | Duration | Features");
                        System.out.println(stringScores[0]+ " | "+ stringScores[1]
                        + " | " + stringScores[2]+ " | " + stringScores[3]);
                        System.out.println("You Win! The song was " + yeezle.getSolution());
                        System.out.println("Do you want to play again? (Y|N)");
                        String input = scanner.nextLine().toUpperCase();
                        if (input.equals("Y")) {
                            mainLoop();
                        }
                        break;
                    } else {
                        System.out.println("Album | Track | Duration | Features");
                        System.out.println("  " + stringScores[0]+ "   |   "+ stringScores[1]
                        + "   |    " + stringScores[2]+ "     |    " + stringScores[3]);
                    }
                } else {
                    System.out.println("Please enter a valid song and try again...");
                }

        }

    } catch (IndexOutOfBoundsException e) {
        System.out.println("The song was: ");
        System.out.println(yeezle.getSolution().toString());
        System.out.println("Do you want to play again? (Y|N)");
        String input = scanner.nextLine().toUpperCase();
        if (input.equals("Y")) {
            mainLoop();
        }
        }
    scanner.close();
    }
    
    public static void main(String[]args) {
        mainLoop();
    }
}
