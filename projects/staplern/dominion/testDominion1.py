# -*- coding: utf-8 -*-
"""
Saturday Jan 18 12:38 2020

@author: Nicholas Stapler
"""

import Dominion
import random
import testUtility
from collections import defaultdict

# Get player names
player_names = testUtility.getPlayerNames(3, True)

# number of curses and victory cards
nV, nC = testUtility.determineVcCcCounts(player_names)

# Define box
box = testUtility.createBox(nV)
# Create an bug where the garden cards
# Are initialized to be 10 just like the other box cards
# by mistake
box["Gardens"] = [Dominion.Gardens()] * 10
supply_order = testUtility.getSupplyOrder()

# Pick 10 cards from box to be in the supply.
supply = testUtility.getRandomSupply(box, player_names, nV, nC)

# initialize the trash
trash = []

# Construct the Player objects
players = testUtility.createPlayerObjects(player_names)
# Play the game
turn = 0
testUtility.playDominionGame(turn, supply, supply_order, trash, players)

# Final score
testUtility.revealFinalScores(players)
