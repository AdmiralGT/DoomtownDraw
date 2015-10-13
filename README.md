# DoomtownDraw
Hand Rank calculator for Doomtown Reloaded decks

Takes a Doomtown deck and determines the average hand rank and hand rank breakdown for a given amount of stud bullets.

Usage:
------
python DoomtownDraw.py filename

Filename must include a complete path to the file if not run from the same directory as DoomtownDraw.py

Optional arguments:
-------------------

* --stud X : X is the number of stud bullets in your posse. The default is 2.

* --iterations X: X is the number of iterations to simulate. The higher this value, the less uncertainty on the average but the longer it will take to calculate. The default is 10000.
              
* --debug: Prints debugging information.             

File format
----------

1 card per line. Cards must be given in the following format Value,Suit. Value is a value from 1 (Ace) to 13 (King). Suit is C (Clubs), D (Diamonds), H (Hearts), S (Spades). 

Jokers are represented by just the text 'Joker' (Current case sensitive).

Minimum of 47 cards, maximum of 54 cards and 2 Jokers.
