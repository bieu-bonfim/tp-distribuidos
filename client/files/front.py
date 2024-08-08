import arcade
import random
import socket
import threading
import time
import client
import json
from arcade.gui import UIManager

host = 'server'
port = 8020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

player_name = input()
ready = input("pronto?")

time.sleep(5)






# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy"
BASE_MARGIN = 30

CARD_SCALE = 0.2
SHOWCASE_CARD_SCALE = 0.35

# How big are the cards?
CARD_WIDTH = 750 * CARD_SCALE
CARD_HEIGHT = 1050 * CARD_SCALE
SHOWCASE_WIDTH = 750 * SHOWCASE_CARD_SCALE
SHOWCASE_HEIGHT = 1050 * SHOWCASE_CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
SHOWCASE_MAT_HEIGHT = int(SHOWCASE_HEIGHT * MAT_PERCENT_OVERSIZE)
SHOWCASE_MAT_WIDTH = int(SHOWCASE_WIDTH * MAT_PERCENT_OVERSIZE)

TOTAL_SCREEN_WIDTH = SCREEN_WIDTH + SHOWCASE_MAT_WIDTH + (BASE_MARGIN*2)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + BASE_MARGIN
# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + BASE_MARGIN
# Card constants

CARD_NAMES = ["bigfoot", "chupacabra", "mothman", "ness", "ufo", "anunnaki", "ashtasheran", "bloop", "fairy", "gnome", 
              "greys", "kraken", "mapinguari", "megalodon", "nightcrawler", "poltergeist", "reptilian", "siren", 
              "skinwalker", "slenderman", "thunderbird", "vampire", "varginha", "wendigo", "werewolf", "witch", "yeti"]

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - (MAT_HEIGHT / 2) - BASE_MARGIN

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * BASE_MARGIN

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * BASE_MARGIN

MIDDLE_SCREEN_X = SCREEN_WIDTH / 2
MIDDLE_SCREEN_Y = SCREEN_HEIGHT / 2

TOP_Y_SHOWCASE = SCREEN_HEIGHT - (SHOWCASE_MAT_HEIGHT / 2) - BASE_MARGIN
END_X = TOTAL_SCREEN_WIDTH - (SHOWCASE_MAT_WIDTH/2) - BASE_MARGIN

FACE_DOWN_IMAGE = "/home/cards/backcard.png"

PILE_COUNT = 3
DRAW = 0
HAND = 1
PLAY = 2

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

class Player():

    def __init__(self, id, name, card, mat):
        self.id = id
        self.name = name
        self.card = card
        self.mat = mat


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.reset_position = False
        self.selected_card = None
        self.piles = None
        self.hand_size = 0
        self.has_selected = False





        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        tipo_button = arcade.gui.UIFlatButton(text="Tipo", width=200)
        self.v_box.add(tipo_button.with_space_around(bottom=15))
        tipo_button.on_click = self.on_click_tipo

        tamanho_button = arcade.gui.UIFlatButton(text="Tamanho", width=200)
        self.v_box.add(tamanho_button.with_space_around(bottom=15))
        tamanho_button.on_click = self.on_click_tamanho

        perigo_button = arcade.gui.UIFlatButton(text="Perigo", width=200)
        self.v_box.add(perigo_button.with_space_around(bottom=15))
        perigo_button.on_click = self.on_click_perigo

        medo_button = arcade.gui.UIFlatButton(text="Medo", width=200)
        self.v_box.add(medo_button.with_space_around(bottom=15))
        medo_button.on_click = self.on_click_medo

        avistamento_button = arcade.gui.UIFlatButton(text="Avistamento", width=200)
        self.v_box.add(avistamento_button.with_space_around(bottom=15))
        avistamento_button.on_click = self.on_click_avistamento

        confirmar_button = arcade.gui.UIFlatButton(text="Escolher Carta", width=200)
        confirmar_button.on_click = self.on_click_confirmar

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

        # List of cards we are dragging with the mouse
        self.held_cards = None
        self.opponents = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        self.p1 = Player(None, None, None, None)
        self.p2 = Player(None, None, None, None)
        self.p3 = Player(None, None, None, None)

        self.opponents.append(self.p2)
        self.opponents.append(self.p3)

        self.p1.name = player_name

       # self.p2_mat = None
       # self.p2_card = None
       # self.p3_mat = None
       # self.p3_card = None

        self.has_sent_message = False
        self.has_interacted_card = False
        self.last_hovered_card = None
        self.current_hovered_card = None

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-50,
                align_x=-195,
                child=confirmar_button
            )
        )

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_x=510,
                align_y=-240,
                child=self.v_box)
        )

    def on_click_confirmar(self, event):
        print("enviar carta")
        if self.has_interacted_card and self.reset_position == False:
            self.has_selected = True
            thread_send = threading.Thread(target=self.send_card, args=(s, self.selected_card.name))
            #thread_receive = threading.Thread(target=self.receive_message, args=(s,))
            thread_send.start()  
            #thread_receive.start()
            self.has_sent_message = True 
            self.has_interacted_card = False


    def on_click_tipo(self, event):
        print("tipo")

    def on_click_tamanho(self, event):
        print("tamanho")

    def on_click_perigo(self, event):
        print("perigo")

    def on_click_medo(self, event):
        print("medo")

    def on_click_tamanho(self, event):
        print("tamanho")

    def on_click_avistamento(self, event):
        print("avistamento")





    
    def setup(self):
        
        thread_receive = threading.Thread(target=self.receive_message, args=(s,))
        thread_receive.start()

        data = {'header': 'player_connection','player_name_register': player_name}
        data_str = json.dumps(data)


        try:
            s.sendall(bytes(data_str,encoding="utf-8"))
        except socket.error as e:
            print(str(e))



        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor((MAT_WIDTH*3), MAT_HEIGHT, arcade.color.ARSENIC)
        pile.position = (START_X+ 510), BOTTOM_Y
        self.pile_mat_list.append(pile)

        #pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.DARK_OLIVE_GREEN)
        #pile.position = START_X + X_SPACING, BOTTOM_Y
        #self.pile_mat_list.append(pile)


        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = MIDDLE_SCREEN_X, (MIDDLE_SCREEN_Y + 120)
        self.pile_mat_list.append(pile)

        # pilha segundo jogador
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = (MIDDLE_SCREEN_X/2), (MIDDLE_SCREEN_Y + 270)
        self.p2.mat = pile

        # pilha terceiro jogador
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.CORDOVAN)
        pile.position = (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X, (MIDDLE_SCREEN_Y + 270)
        self.p3.mat = pile

        pile = arcade.SpriteSolidColor(SHOWCASE_MAT_WIDTH, SHOWCASE_MAT_HEIGHT, arcade.csscolor.GREY)
        pile.position = END_X, TOP_Y_SHOWCASE
        self.pile_mat_list.append(pile)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_name in CARD_NAMES:
            card = Card(card_name, CARD_SCALE)
            card.position = START_X, BOTTOM_Y
            self.card_list.append(card)


        
        self.piles = [[] for _ in range(PILE_COUNT)]

        for card in self.card_list:
            self.piles[DRAW].append(card)

        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

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

    def reorganize_hand(self, pile_index):
        count = 0
        for card in self.piles[pile_index]:
            card.position = (START_X+ 510) + 100 * (count), BOTTOM_Y
            count += 1

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager.draw()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        self.p2.mat.draw()
        self.p3.mat.draw()

        # Draw the cards
        self.card_list.draw()

        arcade.draw_lrtb_rectangle_outline(left=0, right=SCREEN_WIDTH, top=SCREEN_HEIGHT, bottom=0, color=arcade.color.BLACK, border_width=3)

        arcade.draw_text(
            self.p1.name,
            start_x= START_X -80,
            start_y= TOP_Y -100,
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

        if self.current_hovered_card:
            amplified_card = arcade.Sprite(self.current_hovered_card.image_file_name, SHOWCASE_CARD_SCALE)
            amplified_card.position = END_X, TOP_Y_SHOWCASE
            amplified_card.draw()

        if self.p2.card != None and self.p2.name != None:
            self.p2.card.position = (MIDDLE_SCREEN_X/2), (MIDDLE_SCREEN_Y + 270)
            self.p2.card.draw()
            arcade.draw_text(
            self.p2.name,
            start_x= (MIDDLE_SCREEN_X/2),
            start_y= (MIDDLE_SCREEN_Y + 300),
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            anchor_y="center")

        if self.p3.card != None and self.p3.name != None:
            self.p3.card.position = (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X, MIDDLE_SCREEN_Y + 270
            self.p3.card.draw()
            arcade.draw_text(
            self.p3.name,
            start_x= (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X,
            start_y= (MIDDLE_SCREEN_Y + 300),
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            anchor_y="center")

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        self.has_interacted_card = True
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:



            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Save the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        self.reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            pile_index = self.pile_mat_list.index(pile)
            print(pile_index)

            if pile_index == self.get_pile_for_card(self.held_cards[0] or pile_index == DRAW):
                self.reset_position = True
                pass

            elif pile_index == HAND and self.hand_size < 3:
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x + 100 * (i + 1), top_card.center_y 
                        dropped_card.faceUp()
                        print(dropped_card.name)
                        self.hand_size += 1
                else:
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = pile.center_x, pile.center_y
                        dropped_card.faceUp()
                        print(dropped_card.name)
                        self.hand_size += 1

                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                self.reset_position = False

            elif pile_index == PLAY:
                self.held_cards[0].position = pile.position
                for i, dropped_card in enumerate(self.held_cards):   
                    dropped_card.faceUp()
                    print(dropped_card.name)
                    self.selected_card = dropped_card


                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                self.reorganize_hand(HAND)
                self.reset_position = False


            # For each held card, move it to the pile we dropped on
            #for i, dropped_card in enumerate(self.held_cards):
            #    # Move cards to proper position
            #    dropped_card.position = pile.center_x, pile.center_y
            #    dropped_card.faceUp()
            #    print(dropped_card.name)
            #    self.selected_card = dropped_card




            # Success, don't reset position of cards
            #self.reset_position = False

            # Release on top play pile? And only one card held?
        if self.reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

        #if self.has_interacted_card and self.reset_position == False:
        #    thread_send = threading.Thread(target=self.send_card, args=(s, dropped_card.name))
        #    #thread_receive = threading.Thread(target=self.receive_message, args=(s,))
        #    thread_send.start()  
        #    #thread_receive.start()
        #    self.has_sent_message = True 
        #    self.has_interacted_card = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

        # Handle hover action
        self.handle_hover(x, y)

    def handle_hover(self, x, y):
        """ Handle card hover action """
        # Get the card currently under the mouse pointer
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

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    #def send_message(self, client_socket, message):
    #    try:
    #        client_socket.sendall(message.encode())
    #        self.has_sent_message = False
    #    except socket.error as e:
    #        print(str(e))

    def send_message(self, client_socket):
        
        data = {'header': 'player_connection','player_name_register': self.p1.name}
        data_str = json.dumps(data)
        
        try:
            client_socket.sendall(bytes(data_str,encoding="utf-8"))
        except socket.error as e:
            print(str(e))

    def send_card(self, client_socket, card):
        
        data = {'header': 'card_send', 'card': card, 'player_name': self.p1.name}
        data_str = json.dumps(data)
        
        try:
            client_socket.sendall(bytes(data_str,encoding="utf-8"))
        except socket.error as e:
            print(str(e))

            
    def receive_message(self, client_socket):
        while True:
            try:

                data = client_socket.recv(1024)
                print(f"DATA DATA - {data.decode()}")
                data_dict = json.loads(data.decode("utf-8"))
                
                if 'player_name_register' in data_dict:
                    if self.opponents[0].name == None:
                        self.opponents[0].name = data_dict['player_name_register']
                        print(self.opponents[0].name)

                    else:
                        self.opponents[1].name = data_dict['player_name_register']
                        print(self.opponents[1].name)
                            
                if 'card' in data_dict:
                    print(f"Received {data_dict['card']}")
                    print(f"From player {data_dict['player_name']}")

                    self.render_opponent_card(message=data_dict)
            except socket.error as e:
                print(str(e))
                break

    def print_on_timer( ):
        while True:
            print( "Timer Test" )
            time.sleep( 5 )

    def render_opponent_card(self, message):
        for opponent in self.opponents:
            print(f"oponente name: {opponent.name}")
            print(message['player_name'])
            if opponent.name == message['player_name']:
                for card in self.card_list:
                    if card.name == message['card']:
                        opponent.card = arcade.Sprite(FACE_DOWN_IMAGE, CARD_SCALE)



def main():
    """ Main function """
    
    #port = int(input('Enter port: '))

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((host, port))


    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()