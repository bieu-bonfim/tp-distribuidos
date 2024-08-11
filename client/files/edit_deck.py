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
    def __init__(self):
        super().__init__()
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


    def setup(self):
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        self.card_list = arcade.SpriteList()
        self.deck1 = arcade.SpriteList()
        self.deck2 = arcade.SpriteList()
        self.deck3 = arcade.SpriteList()
        self.deck_list = self.deck1
        
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


        pile = arcade.SpriteSolidColor(SHOWCASE_MAT_WIDTH, SHOWCASE_MAT_HEIGHT, arcade.csscolor.GREY)
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


        for card_name in CARD_NAMES:
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
            
    def on_click_salvar(self, event):
        print("salvar")

    def on_click_escolher(self, event):
        print("Escolher")

    def on_click_deck1(self, event):
        self.choosed_deck = 1

    def on_click_deck2(self, event):
        self.choosed_deck = 2

    def on_click_deck3(self, event):
        self.choosed_deck = 3

    def on_click_voltar(self, event):
        menu = main_menu.MainMenu()
        self.window.show_view(menu)

    def on_draw(self):
        self.clear()
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