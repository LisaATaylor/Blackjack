# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 13:01:54 2018

@author: LACKERMAN
"""
import random

class Card:
    """
    An individual playing card.  Assumes input attributes are valid.
    
    Attributes:
        val (str):  card value as string (i.e. 'A', '2', 'K')
        suit (str): one of 'Heart','Diamond','Spade','Club'
        name (str): readable card name
        blackjack_value (int):  point value of card, aces have value 'A'=11 or 'a'=1
        
    """
    def __init__(self, val, suit):
        self.val=val
        self.suit=suit
        self.name= self.suit + ' '+ self.val
        def __bjval(self):
            if self.val in 'JQK':
                n= 10
            elif self.val =='A':
                n= 11
            elif self.val =='a':
                n=1
            else:
                n=int(self.val)
            return n
        self.blackjack_value=__bjval(self)

class Deck: 
    '''
    Deck of cards composed of ndeck individual decks
    
    Attributes:
        ndeck (int): Number of decks needed for game
        cards (list):  List of individual cards remaining in the deck 
    
    Deck.cards is ordered until running Deck.shuffle() to randomize
    '''
    def __init__(self,ndeck):
        self.ndeck=ndeck
        self.vals_in_game = [(x if x!='0' else '10') for x in 'A234567890JQK'] #could tweak this for decks for different games
        self.suits_in_game = ['Heart','Diamond','Spade','Club']
        self.cards=[Card(val,suit) for val in self.vals_in_game for suit in self.suits_in_game]*ndeck #ordered list of cards
    def shuffle(self):
        ''' Randomizes the deck'''
        ncards=len(self.cards)
        cpos=random.sample(range(ncards),ncards)#generate random list of card positions
        self.cards=[self.cards[pos] for pos in cpos]
    def deal(self,ncards=1):
        '''Deals out cards
           Argument:  
               ncard (int):  Number of cards to deal
           Returns: List of Card objects of length ncards
        '''
        dealtcards = [] 
        while ncards>0:
            dealtcard=self.cards.pop()
            dealtcards=dealtcards+[dealtcard]
            ncards-=1
        return dealtcards
    
class Player:
    '''Game player named pn
       Parameter:
           pname (str):  Player name
           hand (list):  List of Cards held by player
           busted (bool):  Whether player has busted
    '''
    def __init__(self,pname):
        self.name=pname
        self.hand=[]
        self.busted=False
    def draw(self,ncards,deck_obj):
        '''
        Recieve cards from Deck
        
        Arguments:
            ncards (int): number of cards to draw
            deck_obj:  Deck to draw from
        
        Updates:
            Player.hand
            
        '''
        newcards=deck_obj.deal(ncards)
        self.hand.extend(newcards)
      
    def hand_value(self):
        '''calculates held value of cards in hand'''
        cardvals=[c.blackjack_value for c in self.hand]
        return sum(cardvals)  
    def hand_txt(self):
        ''' generates list of cards'''
        return ' '.join(x.name for x in self.hand)
    def convert_ace(self):
        '''tests for ace in hand, converts 'A' (11) to 'a' (1)'''
        try:
            aceix=[c.val for c in self.hand].index('A') #returns valueerror if no match
            print('{} busted with at least one ace.  Converted one ace from 11 to 1'.format(self.name))
            acesuit=self.hand[aceix].suit
            del self.hand[aceix]
            self.hand.append(Card('a',acesuit))#add back ace with value=1
        except:
            pass
            
class BlackjackGame:
    '''Initiates the game, holds all objects associated with the game
    Parameters:
        BlackjackGame.player (Player)
        BlackjackGame.dealer (Player)
        BlackjackGame.deck (Deck)
    
    '''
    
    def __init__(self):
        self.player=Player('player') #single player game
        self.dealer=Player('dealer')
        self.deck=Deck(2)
        self.deck.shuffle()
        self.player.draw(2,self.deck)
        if self.player.hand_value()==22:#in case drew 2 aces in first draw, convert one from 11 to 1
            self.player.convert_ace()
            
    def status_msg(self):
        print('Player hand contains: '+', '.join([c.name for c in self.player.hand]) +' for a total of: '+str(self.player.hand_value()))

#start game
if __name__=='__main__':
    bjgame=BlackjackGame()
    
    #play player
    while not bjgame.player.busted:
        bjgame.status_msg()
        sel = input('Enter h to hit or anything else to stand: ')
        if sel=='h':
            bjgame.player.draw(1,bjgame.deck)
            if bjgame.player.hand_value()>21:
                bjgame.player.convert_ace()
                #bjgame.status_msg()
                if bjgame.player.hand_value()<=21:
                    continue
                else:
                    bjgame.player.busted=True
                    bjgame.status_msg()
                    print('BUSTED!  Game over.')
        else: #stand
            break
    
    if not bjgame.player.busted:
        #play dealer
        print('Playing dealer')
        bjgame.dealer.draw(2,bjgame.deck)
        while bjgame.dealer.hand_value()<17: #keep dealing until dealer breaks 17
            bjgame.dealer.draw(1,bjgame.deck)
            if bjgame.dealer.hand_value()>21:
                bjgame.dealer.convert_ace()
            else:
                continue
        bjgame.dealer.busted=True if bjgame.dealer.hand_value()>21 else False
        print('Dealer holding '+bjgame.dealer.hand_txt())
        if bjgame.dealer.busted:
            print('Dealer busted with {}.  You win!'.format(bjgame.dealer.hand_value()))
            
    if not (bjgame.dealer.busted or bjgame.player.busted):#neither dealer or player busted
        if bjgame.player.hand_value()<bjgame.dealer.hand_value():
            print('Dealer has '+str(bjgame.dealer.hand_value())+'\nDealer wins :(')
        elif bjgame.player.hand_value()>bjgame.dealer.hand_value():
            print('Dealer has '+str(bjgame.dealer.hand_value())+'\nYou win :)')
        else:
            print('You both have '+str(bjgame.dealer.hand_value())+'\nIts a draw')

    




