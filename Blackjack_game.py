import random, time


class Deck:
    D = '\u2666'
    H = '\u2665'
    C = '\u2663'
    S = '\u2660'

    number = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = [D, H, C, S]
    def __init__(self) -> None:
        self.cards = [f'{num}{suit}' for num in Deck.number for suit in Deck.suits]
        self.card_values = self.get_card_values()


    def get_card_values(self):
        values = dict()
        for card in self.cards:
            if card[0].isdigit():
                values[card] = int(card[0])

            elif card[0] in ['T', 'J', 'Q', 'K']:
                values[card] = 10

            elif card[0] == 'A':
                values[card] = 11 
        
        return values
    
    def dealing_cards(self, cards_num):
        dealt_cards = list()
        random.shuffle(self.cards)
        if cards_num == 2:
            for _ in range(cards_num):
                card = random.choice(self.cards)
                dealt_cards.append(card)
                self.cards.remove(card)

            return dealt_cards
        else:
            card = random.choice(self.cards)
            self.cards.remove(card)
            return card

    def counting_values(self, lst):
        total_lst = list()
        for card in lst:
            value = self.card_values[card]
            total_lst.append(value)
        
        total = sum(total_lst)

        for card in lst:
            if total > 21 and card[0] == 'A':
                total -= 10
        
        return total


class Game:
    def __init__(self):
        self.player_cards_lst = []
        self.dealer_cards_lst = []

        self.player_string_cards = ''
        self.dealer_string_cards = ''

        self.player_money = 500
        self.running = True

        self.player_bust = False
        self.dealer_bust = False
    
    def answer_to_play(self):
        while True:
            answer = input(f'You are starting with ${self.player_money}, would you like to play? ')
            if answer not in ['yes', 'y', 'no', 'n']:
                print('Please type yes or no')
                continue
            else:
                break
        if answer in ['no', 'n']:
            print('Ok, see you later!')
            return False
        
        return True

    def handling_bet(self):
        while True:
            try:
                bet = float(input('Place your bet: '))
            except:
                print('Please type a number')
                continue
            if bet < 1:
                print('The minimum bet is $1.')
                continue
            elif bet > self.player_money:
                print('You do not have sufficient funds.')
                continue
            else:
                break
        self.player_money -= bet

        return bet

    def win_hand(self, total):
        if total == 21:
            return True
        else:
            return False

    def stay_or_hit(self):
        while True:
            answer = input('Would you like to hit or stay? ')
            if answer not in ['stay', 'hit']:
                print('That is not a valid option.')
                continue
            else:
                break
        if answer == 'stay':
            return 'stay'
        else:
            return 'hit'

    def main(self):
        print('Welcome to Blackjack!\n')
        while self.running:
            deck = Deck()
            if self.player_money < 1:
                print("You've ran out of money. Please restart this program to try again. Goodbye.")
                self.running = False
                break
            self.running = self.answer_to_play()
            if self.running == False:
                break
            
            self.bet = self.handling_bet()

            #First deal
            self.player_cards_lst = deck.dealing_cards(2)
            self.dealer_cards_lst = deck.dealing_cards(2)
            self.player_string_cards = ' , '.join(self.player_cards_lst)
            self.dealer_string_cards = ' , '.join(self.dealer_cards_lst)
            print(f'You are dealt: {self.player_string_cards} ') 
            print(f'The dealer is dealt: {self.dealer_cards_lst[0]} , Unknown')
            
            self.player_total = deck.counting_values(self.player_cards_lst)
            self.dealer_total = deck.counting_values(self.dealer_cards_lst)

            #Natural blackjack in the first round
            if self.win_hand(self.player_total) and not self.win_hand(self.dealer_total):
                time.sleep(1)
                print(f'The dealer has: {self.dealer_cards_lst[0]} , {self.dealer_cards_lst[1]}')
                new_money = (self.bet * 2) + (self.bet / 2)
                self.player_money += new_money
                time.sleep(1)
                print(f'Blackjack! You win ${self.bet + (self.bet / 2)} :)\n')
                continue
            
            #Tie with natural blackjack
            elif self.win_hand(self.player_total) and self.win_hand(self.dealer_total):
                time.sleep(1)
                print(f'The dealer has: {self.dealer_cards_lst[0]} , {self.dealer_cards_lst[1]}')
                self.player_money += self.bet
                print('You tie. Your bet has been returned.\n')
                continue
            
            #Player's turn
            while True:
                self.player_bust = False
                answer = self.stay_or_hit()
                if answer == 'stay':
                    break 
                
                card = deck.dealing_cards(1)
                self.player_cards_lst.append(card)
                self.player_total = deck.counting_values(self.player_cards_lst)
                self.player_string_cards += f' , {card}'
                print(f'You are dealt: {card}')
                print(f'You now have: {self.player_string_cards}')
                if self.player_total <= 21:
                    continue
                elif self.player_total > 21:
                    print(f'Your hand value is over 21 and you lose ${self.bet} :(\n')
                    self.player_bust = True
                    break
            
            if self.player_bust == True:
                continue
            
            #Dealer's turn
            while True:
                self.dealer_bust = False
                print(f'The dealer has: {self.dealer_string_cards}')
                if self.dealer_total <= 16:
                    time.sleep(1)
                    dealer_card = deck.dealing_cards(1)
                    self.dealer_cards_lst.append(dealer_card)
                    self.dealer_total = deck.counting_values(self.dealer_cards_lst)
                    self.dealer_string_cards += f' , {dealer_card}'
                    print(f'The dealer hits and is dealt: {dealer_card}')
                    continue

                elif 16 < self.dealer_total <= 21:
                    time.sleep(1)
                    print('The dealer stays')
                    break

                elif self.dealer_total > 21:
                    time.sleep(1)
                    print(f'The dealer busts, you win ${self.bet} :)\n')
                    self.player_money += self.bet * 2
                    self.dealer_bust = True
                    break
            
            if self.dealer_bust == True:
                continue
            
            #Compare the values of the player and the dealer
            if self.player_total > self.dealer_total:
                print(f'You win ${self.bet}\n')
                self.player_money += self.bet * 2
            
            elif self.player_total < self.dealer_total:
                print(f'The dealer wins, you lose ${self.bet}\n')
            
            elif self.player_total == self.dealer_total:
                print('You tie. Your bet has been returned.\n')
                self.player_money += self.bet 
             


game = Game()
game.main()




