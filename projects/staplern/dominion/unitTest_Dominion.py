from unittest import TestCase

import Dominion
import  testUtility

class TestAction_card(TestCase):
    def setUp(self):
        self.actionCard = Dominion.Market()
        self.player = Dominion.Player("joe")
        self.player.hand.append(self.actionCard)
        self.player.actions = 0
        self.player.buys = 1
        self.player.purse = 0
        self.addedCard = Dominion.Village()
        self.player.deck = [self.addedCard]
        self.trash = []

    def test_init(self):
        marketCard = Dominion.Market()
        self.assertEqual(marketCard.actions,1)
        self.assertEqual(marketCard.buys, 1)
        self.assertEqual(marketCard.cards, 1)
        self.assertEqual(marketCard.coins, 1)

    def test_use(self):
        self.setUp()
        self.actionCard.use(self.player,self.trash)
        self.assertIn(self.actionCard,self.player.played)
        self.assertNotIn(self.actionCard,self.player.hand)

    def test_augment(self):
        self.setUp()
        self.actionCard.augment(self.player)
        self.assertEqual(self.player.actions,1)
        self.assertEqual(self.player.buys, 2)
        self.assertEqual(self.player.purse, 1)
        self.assertEqual(self.player.deck, [])
        self.assertIn(self.addedCard, self.player.hand)


class TestPlayer(TestCase):
    def setUp(self):
        self.player = Dominion.Player("joe")
        self.trash = []

    def test_draw(self):
        self.setUp()
        self.poppedCard = Dominion.Chancellor()
        self.player.deck = [self.poppedCard]
        self.discardCard = Dominion.Village()
        self.player.discard = [self.discardCard]

        self.player.draw()
        self.assertIn(self.poppedCard,self.player.hand)
        self.player.draw()
        self.assertEqual(self.player.discard,[])
        self.assertIn(self.discardCard,self.player.hand)
        newCard = Dominion.Thief()
        self.player.discard = [newCard]
        virtualHand=[]
        self.player.draw(virtualHand)
        self.assertIn(newCard,virtualHand)
        self.assertNotIn(newCard,self.player.discard)

    def test_action_balance(self):
        self.setUp()
        self.player.discard=[Dominion.Village(),Dominion.Village()]
        actionBal =self.player.action_balance()
        self.assertEqual(actionBal,(70*2 / len(self.player.stack())))

    def test_cardsummary(self):
        self.setUp()
        cardSummary = self.player.cardsummary()
        self.assertEqual(cardSummary["Copper"],7)
        self.assertEqual(cardSummary["Estate"], 3)
        self.assertEqual(cardSummary["VICTORY POINTS"], 3)
        self.player.discard=[Dominion.Province()]
        cardSummary = self.player.cardsummary()
        self.assertEqual(cardSummary["Copper"], 7)
        self.assertEqual(cardSummary["Estate"], 3)
        self.assertEqual(cardSummary["Province"], 1)
        self.assertEqual(cardSummary["VICTORY POINTS"], 9)


    def test_calcpoints(self):
        self.setUp()
        self.player.discard=[Dominion.Gardens(),Dominion.Gardens()]
        points = self.player.calcpoints()
        self.assertEqual(points,5) #3 estates and 12 cards in stack



class TestGameOver(TestCase):
    def setUp(self):
        # Get player names
        player_names = testUtility.getPlayerNames(3, True)

        # number of curses and victory cards
        nV, nC = testUtility.determineVcCcCounts(player_names)

        # Define box
        box = testUtility.createBox(nV)

        supply_order = testUtility.getSupplyOrder()

        # Pick 10 cards from box to be in the supply.
        self.supply = testUtility.getRandomSupply(box, player_names, nV, nC)

    def test_gameover(self):
        self.setUp()
        self.supply["Estate"] = []
        self.supply["Duchy"] = []
        self.assertFalse(Dominion.gameover(self.supply))
        self.supply["Gold"] = []
        self.assertTrue(Dominion.gameover(self.supply))

        self.setUp()
        self.supply["Province"] = []
        self.assertTrue(Dominion.gameover(self.supply))
