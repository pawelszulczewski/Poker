import random
from functools import total_ordering

faces = {'2':2,'3':3,'4':4,'5':5,'6':6, '7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
rev_faces = {y:x for x,y in faces.items()}
suits = ['S','C','D','H']
s_score = {'S':'Spades','C':'Clubs','D':'Diamonds','H':'Hearts'}
scores = {1:'a highest card',2:'a pair',3:'two pairs',4:'three-of-a-kind',5:'a straight',6:'a flush',7:'a fullhouse',8:'four-of-a-kind',9:'a straight-flush'}

class game(object):
	def __init__(self,players,deck,discard):
		self.players = players
		self.deck = deck
		self.discard = discard
	def winner(self,players):
		results = {}
		for player in players:
			self.scorer = scorer(player)
			results[player.name] = (self.scorer.result())
		score = sorted([(value,key) for (key,value) in results.items()])
		score.reverse()
		winscore = score[0]
		if winscore[0][0] != 6:
			out = "Winner is " + winscore[1]+" with "+ scores[winscore[0][0]]+" of "+str(rev_faces[winscore[0][1]])
		else:
			out = "Winner is " + winscore[1]+" with "+ s_scores[winscore[0][0]]+" of "+str(rev_faces[winscore[0][1]])
		return (out)
	def replace(self,player,cards):
		for i in cards:
			player.discard(self.discard,int(i)-1)
			player.insert(self.deck, int(i)-1)
		print(player)
	def play(self):
		for player in players:
			player.draw(deck,5)
			print(player)
			to_replace = input(player.name+", Enter the number of the cards you wish to replace(seperate with commas): ")
			to_replace = to_replace.split(',')
			if (to_replace) != [""]:
				self.replace(player,to_replace)
			print('\n')
		print(self.winner(self.players))
		for player in players:
			player.clear(self.discard)

class scorer(object):
	def has_flush(self):
		return [all(self.cards[i].suit == self.cards[0].suit for i in range(len(self.cards))),self.cards[0].suit]
	def has_match(self,n,x=1):
		matches = set()
		for i in range(len(self.cards)):
			c1 = self.cards[i]
			cur = 1
			for c2 in self.cards:
				if c1.value ==	c2.value and c1 != c2:
					cur += 1
			if cur == n:
				matches.add(faces[c1.value])
		if len(matches) == x:
			return([True,max(matches)])
		else:
			return([False,0])
	def has_pair(self):
		return self.has_match(2)
	def has_2pair(self):
		return self.has_match(2,2)
	def has_three(self):
		return self.has_match(3)
	def has_four(self):
		return self.has_match(4)	
	def has_fullhouse(self):
		t = self.has_three()
		p = self.has_pair()
		result = t[0] and p[0]
		if result:
			return [result, max([t[1], p[1]])]
		else:
			return[result,0]
	def has_straight(self):
		nums = sorted([faces[c.value] for c in self.cards])
		result = all(nums[i+1] - nums[i] == 1 for i in range(len(nums)-1)) 
		if result:
			return [result, max(nums)]
		else:
			return [result, 0]
	def has_straightflush(self):
		s = self.has_straight()
		f = self.has_flush()
		result = s[0] and f[0]
		if result:
			return[result, s[1] ]
		else:
			return[result,0]
	def max_card(self):
		return[True, max(faces[card.value] for card in self.cards)]
	def __init__(self,player):
		self.player = player
		self.cards = player.hand
		self.checkers = [self.has_straightflush, self.has_four, self.has_fullhouse, self.has_flush, self.has_straight, self.has_three, self.has_2pair, self.has_pair, self.max_card]
	def result(self):
		results = [self.checkers[i]() for i in range(len(self.checkers))]
		for i in range(len(self.checkers)):
			if results[i][0]:
				return[9-i,results[i][1], max(faces[card.value] for card in self.cards)]
				break

@total_ordering
class Card(object):
	def __init__(self,val,suit):
		self.value = val
		self.suit = suit
	def __str__(self):
		return (str(self.value)+self.suit)
	def __gt__(self,other):
		if (suits.index(self.suit)) != suits.index(other.suit):
			return suits.index(self.suit) > suits.index(other.suit)
		else:
			return faces[self.value] > faces[other.value]
	def  __eq__(self,other):
		return (self.suit == other.suit and self.value == other.value)

class Deck(object):
	def new_deck(self):
		self.cards = []
		if not self.discard:
			for suit in suits:
				for val in faces.keys():
					self.cards.append(Card(val,suit))
			self.shuffle()
	def __init__(self,discard=False):
		self.discard = discard
		self.new_deck()
	def draw(self,n):
		self.drawn = []
		for i in range(n):
			self.drawn.append(self.cards.pop(0))
		return(self.drawn)
	def shuffle(self):
		random.shuffle(self.cards)
	def sort(self):
		self.sort(self.cards)
	def add(self,card,shfl=False):
		self.cards.append(card)
		if shfl:
			self.shuffle(self.cards)
	def view(self):
		return(self.cards)
	def count(self):
		return(str(len(self.cards)))
	def __str__(self):
		return(self.count()+" cards left in deck: " + ' '.join([str(card) for card in self.view()]))

class Player(object):
	def __init__(self,name):
		self.hand = []
		self.name = name
		self.wins = 0
	def draw(self,deck,num):
		for card in deck.draw(num):
			self.hand.append(card)
	def discard(self,discard,num):
		discard.add(self.hand.pop(num))
	def insert(self,deck,num):
		self.hand.insert(num,deck.draw(1)[0])
	def __str__(self):
		return("Player: " +self.name + ". Cards: " + ' '.join([str(card) for card in self.view()]))
	def view(self):
		return (self.hand)
	def clear(self,discard):
		for i in range(len(self.hand)):
			self.discard(discard,0)
	def add_win(self,n):
		self.wins += n 
	def order(self):
		self.hand.sort()


deck = Deck()
discard = Deck(discard=True)
playing = (input("Do you wish to play? (Y/n) "))
if playing[0] == 'Y' or playing[0] == 'y':
	names = input("Enter player names (seperate with commas) ").split(',')
	while names == ['']:
		print("Please enter at least 2 names")
		names = input("Enter player names (seperate with commas) ").split(',')
	players = [Player(name) for name in names]
	g1 = game(players,deck,discard)
while playing[0] == 'Y' or playing[0] == 'y':
	print("Shuffling deck",'\n')
	deck.new_deck()
	g1.play()
	playing = (input("Do you wish to play again? "))
