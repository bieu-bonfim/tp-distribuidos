import socket
import threading
import time
import client
import json
import login
import arcade
import arcade.gui
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import main_menu

# screen width - 1412
CARD_SCALE = 0.2
SHOWCASE_CARD_SCALE = 0.35

# How big are the cards?
CARD_WIDTH = 750 * CARD_SCALE
CARD_HEIGHT = 1050 * CARD_SCALE
SHOWCASE_WIDTH = 750 * SHOWCASE_CARD_SCALE
SHOWCASE_HEIGHT = 1050 * SHOWCASE_CARD_SCALE
BASE_MARGIN = 30

SCREEN_WIDTH = 1412
SCREEN_HEIGHT = 868


# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
SHOWCASE_MAT_HEIGHT = int(SHOWCASE_HEIGHT * MAT_PERCENT_OVERSIZE)
SHOWCASE_MAT_WIDTH = int(SHOWCASE_WIDTH * MAT_PERCENT_OVERSIZE)

START_X = MAT_WIDTH / 2 + BASE_MARGIN

TOP_Y_SHOWCASE = SCREEN_HEIGHT - (SHOWCASE_MAT_HEIGHT / 2) - BASE_MARGIN
END_X = SCREEN_WIDTH - (SHOWCASE_MAT_WIDTH/2) - BASE_MARGIN

FACE_DOWN_IMAGE = "/home/cards/backcard.png"
CARD_NAMES = ["bigfoot", "chupacabra", "mothman", "ness", "ufo", "anunnaki", "ashtasheran", "bloop", "fairy", "gnome", 
              "greys", "kraken", "mapinguari", "megalodon", "nightcrawler", "poltergeist", "reptilian", "siren", 
              "skinwalker", "slenderman", "thunderbird", "vampire", "varginha", "wendigo", "werewolf", "witch", "yeti"]

PILE_COUNT = 5
CARDS1 = 0
CARDS2 = 1
DECK1 = 2
DECK2 = 3
DECK3 = 4

sem = threading.Semaphore()

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self,name, scale=CARD_SCALE):
        """ Card constructor """

        # Attributes for suit and value
        self.name = name

        # Image to use for the sprite when face up
        self.image_file_name = f"/home/cards/{name}.png"
        self.is_face_up = False

        # Call the parent
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def faceUp(self):
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    def faceDown(self):
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def isFaceUp(self):
        if self.is_face_up == True:
            return True
        else:
            return False

    @property
    def isFaceDown(self):
        return not self.is_face_up

class EditDeck(arcade.View):
    def __init__(self, client, data_chunk):
        super().__init__()
        self.data_chunk = data_chunk
        self.client = client
        self.pile_mat_list = None
        self.piles = None
        self.card_list = None
        self.manager = arcade.gui.UIManager()
        self.manager.disable()
        self.held_cards = None
        self.held_cards_deck = None
        self.v_box = arcade.gui.UIBoxLayout()
        self.last_hovered_card = None
        self.current_hovered_card = None
        self.deck_list = None
        self.deck1 = None
        self.deck2 = None
        self.deck3 = None
        self.choosed_deck = 1
        self.background = arcade.load_texture("/home/sprites/edit_deck_screen.png")
        self.cards_array = data_chunk['cards']
        self.deck1_cards = data_chunk['decks'][0]['cards']
        self.deck1_id = data_chunk['decks'][0]['deck_id']
        self.deck2_cards = data_chunk['decks'][1]['cards']
        self.deck2_id = data_chunk['decks'][1]['deck_id']
        self.deck3_cards = data_chunk['decks'][2]['cards']
        self.deck3_id = data_chunk['decks'][2]['deck_id']
        self.selected_deck_id = None

    def setup(self):
        threading.Thread(target=self.receive_message).start()
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        self.card_list = arcade.SpriteList()
        self.deck1 = arcade.SpriteList()
        self.deck2 = arcade.SpriteList()
        self.deck3 = arcade.SpriteList()
        self.deck_list = self.deck1
        
        # --------------------------
        # --------------------------
        print(self.cards_array)
        self.held_cards = []

        self.v_box = arcade.gui.UIBoxLayout()
        self.deck_box = arcade.gui.UIBoxLayout()

        deck1_button = arcade.gui.UIFlatButton(text="Deck 1", width=200, height = 30)
        self.deck_box.add(deck1_button.with_space_around(bottom=15))
        deck1_button.on_click = self.on_click_deck1

        deck2_button = arcade.gui.UIFlatButton(text="Deck 2", width=200, height = 30)
        self.deck_box.add(deck2_button.with_space_around(bottom=15))
        deck2_button.on_click = self.on_click_deck2

        deck3_button = arcade.gui.UIFlatButton(text="Deck 3", width=200, height = 30)
        self.deck_box.add(deck3_button.with_space_around(bottom=15))
        deck3_button.on_click = self.on_click_deck3

        tipo_button = arcade.gui.UIFlatButton(text="Salvar Deck", width=200, height = 40)
        self.v_box.add(tipo_button.with_space_around(bottom=15))
        tipo_button.on_click = self.on_click_salvar

        tamanho_button = arcade.gui.UIFlatButton(text="Escolher Deck", width=200, height = 40)
        self.v_box.add(tamanho_button.with_space_around(bottom=15))
        tamanho_button.on_click = self.on_click_escolher

        tamanho_button = arcade.gui.UIFlatButton(text="Voltar", width=200, height = 40)
        self.v_box.add(tamanho_button.with_space_around(bottom=15))
        tamanho_button.on_click = self.on_click_voltar

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = START_X, TOP_Y_SHOWCASE + 100
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = START_X + MAT_WIDTH, TOP_Y_SHOWCASE + 100
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.ARSENIC)
        pile.position = START_X + (MAT_WIDTH*2.5) + 150, TOP_Y_SHOWCASE + 100
        self.pile_mat_list.append(pile)


        pile = arcade.Sprite("/home/sprites/preview_card_mat.png", scale=0.35)
        pile.position = END_X, TOP_Y_SHOWCASE
        self.pile_mat_list.append(pile)
        
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_x= 40,
                align_y= -320,
                child=self.deck_box)
        )

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_x=510,
                align_y=-320,
                child=self.v_box)
        )

        for card_name in self.cards_array:
            card = Card(card_name, CARD_SCALE)
            card.position = START_X, TOP_Y_SHOWCASE
            self.card_list.append(card)
            card.faceUp()

        self.piles = [[] for _ in range(PILE_COUNT)]

        count = 0
        for card in self.card_list:
            if count < 20:
                self.piles[CARDS1].append(card)
                count += 1
            else:
                self.piles[CARDS2].append(card)

        for card in self.deck1_cards:
            print(card)
            card = Card(card, CARD_SCALE)
            self.deck1.append(card)
            card.faceUp()
            self.piles[DECK1].append(card)
            self.show_deck(DECK1)

        for card in self.deck2_cards:
            print(card)
            card = Card(card, CARD_SCALE)
            self.deck2.append(card)
            card.faceUp()
            self.piles[DECK2].append(card)
            self.show_deck(DECK2)

        for card in self.deck3_cards:
            print(card)
            card = Card(card, CARD_SCALE)
            self.deck3.append(card)
            card.faceUp()
            self.piles[DECK3].append(card)
            self.show_deck(DECK3)
    
        count = 0
        for card in self.piles[CARDS1]:
            if count < 20:
                card.position = START_X, (TOP_Y_SHOWCASE + 100) - (30*count)
                count += 1
            else:
                break

        count = 0
        for card in self.piles[CARDS2]:
            card.position = START_X + MAT_WIDTH, (TOP_Y_SHOWCASE + 100) - (30*count)
            count += 1
            
        self.selected_deck_id = self.deck1_id

    def on_click_salvar(self, event):
        if len(self.deck_list) < 9:
            print("Deck precisa ter 9 cartas!")
        else:
            names = []
            for name in self.deck_list:
                names.append(name.name)

            send_deck = {
                    "header": "edit_deck",
                    "request": {
                    "deck_id": self.selected_deck_id,
                    "cards": names
                    }
                }
            
            self.client.sendMessage(send_deck)
            print(send_deck)
            print("salvar")

    def on_click_escolher(self, event):
        self.client.client_deck = self.selected_deck_id
        data = {'header': 'choose_deck', 'request': {'deck_id': self.selected_deck_id}}
        self.client.sendMessage(data)
        cards_to_add = []
        for card in self.deck_list:
            cards_to_add.append(card.name)
        print("cartas escolhidas", cards_to_add)
        self.client.selected_deck_cards = cards_to_add
        print("Escolher")

    def on_click_deck1(self, event):
        self.choosed_deck = 1
        self.selected_deck_id = self.deck1_id

    def on_click_deck2(self, event):
        self.choosed_deck = 2
        self.selected_deck_id = self.deck2_id

    def on_click_deck3(self, event):
        self.choosed_deck = 3
        self.selected_deck_id = self.deck3_id

    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.client)
        self.window.show_view(menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        self.pile_mat_list.draw()
        self.card_list.draw()
        if self.choosed_deck == 1:
            self.deck_list = self.deck1
            self.deck_list.draw()
        if self.choosed_deck == 2:
            self.deck_list = self.deck2
            self.deck_list.draw()
        if self.choosed_deck == 3:
            self.deck_list = self.deck3
            self.deck_list.draw()

        if self.current_hovered_card:
            amplified_card = arcade.Sprite(self.current_hovered_card.image_file_name, SHOWCASE_CARD_SCALE)
            amplified_card.position = END_X, TOP_Y_SHOWCASE
            amplified_card.draw()

        
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        #for card in self.held_cards:
        #    card.center_x += dx
        #    card.center_y += dy

        # Handle hover action
        self.handle_hover(x, y)

    def handle_hover(self, x, y):
        """ Handle card hover action """
        cards = arcade.get_sprites_at_point((x, y), self.card_list)



        # If hovering over a card, change its appearance or perform an action
        if len(cards) > 0:
            hovered_card = cards[-1]

            # Check if this card is already hovered
            if self.last_hovered_card != hovered_card:
                if self.last_hovered_card is not None:
                    self.last_hovered_card.alpha = 255  # Reset previous hovered card
                #hovered_card.alpha = 200  # Example action: Change transparency
                self.last_hovered_card = hovered_card

            # Update the current hovered card for drawing the amplified image
            if hovered_card.isFaceUp() == True:
                self.current_hovered_card = hovered_card

        else:
            # Reset the last hovered card if no card is under the mouse pointer
            if self.last_hovered_card is not None:
                self.last_hovered_card.alpha = 255
                self.last_hovered_card = None

            # Clear the current hovered card if no card is under the mouse pointer
            #self.current_hovered_card = None


    def on_mouse_press(self, x, y, button, modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        cards_deck = arcade.get_sprites_at_point((x, y), self.deck_list)
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            self.held_cards = [primary_card]

            # All other cases, grab the face-up card we are clicking on


            # Save the position
            # Self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            if self.held_cards[0] in self.piles[CARDS1] or self.held_cards[0] in self.piles[CARDS2]:
                print(self.held_cards[0].name)
                card = Card(self.held_cards[0].name, CARD_SCALE)
                self.add_card(card, self.choosed_deck + 1)

        
        elif len(cards_deck) > 0:
            primary_card_deck = cards_deck[-1]
            self.held_cards_deck = [primary_card_deck]

            if self.held_cards_deck[0] in self.piles[self.choosed_deck + 1]:
                print("Deletar")
                self.remove_card(self.held_cards_deck[0], self.choosed_deck + 1)




        #for card_name in CARD_NAMES:
        #    card = Card(card_name, CARD_SCALE)
        #    card.position = START_X, TOP_Y_SHOWCASE
        #    self.card_list.append(card)
        #    card.faceUp()


    def remove_card(self, del_card, pile_index):
        self.piles[pile_index].remove(del_card)
        self.deck_list.remove(del_card)
        self.show_deck(pile_index)

    def get_pile_for_card(self, card):
        for index, pile in enumerate(self.piles):
            if card in pile:
                print("checkpoint")
                return index
            
    def remove_card_from_pile(self, card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_new_pile(self, card, pile_index):
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def add_card(self, card, pile_index):
        if self.is_valid_card(card, pile_index):
            self.piles[pile_index].append(card)
            self.deck_list.append(card)
            card.faceUp()
            self.show_deck(pile_index)

    def is_valid_card(self, card, pile_index):
        count = 0
        for card_search in self.piles[pile_index]:
            if card_search.name == card.name:
                count += 1
        
        if count == 3:
            return False
        elif count < 3 and len(self.piles[pile_index]) < 9:
            return True

    def show_deck(self, pile_index):
        count = 0
        for card in self.piles[pile_index]:
            card.position = START_X + (MAT_WIDTH*2.5) + 150, (TOP_Y_SHOWCASE + 100) - (30*count)
            count += 1

        
        

    def on_show_view(self):
        self.manager.enable()
        print("show deck")

    def on_hide_view(self):
        self.manager.disable()
        print("hide deck")

    def receive_message(self):
        while True:
            try:
                data_dict = self.client.receiveMessage()
                print(data_dict)
                
                if data_dict['header'] == 'choose_deck':
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)          
                    break
            except Exception as e:
                print(str(e))
                


