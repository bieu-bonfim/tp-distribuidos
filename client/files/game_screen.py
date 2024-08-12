import arcade
import random
import socket
import threading
import time
import json
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
from client import Client

host = 'server'
port = 8020

# = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host, port))

#player_name = input()
#ready = input("pronto?")

#time.sleep(5)






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

CARD_NAMES = ["Alien grey", "Anunnaki", "Ashtar Sheran", "Bruxa", "Chupacabra", "ET de Varginha", "Fada", "Fresno Nightcrawler", "Gnomo", "Kraken", 
              "Lobisomem", "Mapinguari", "Megalodon", "Monstro do Lago Ness", "Mothman", "O Bloop", "Passaro Trovao", 
              "Pe Grande", "Poltergeist", "Reptlianos", "Sereia", "Skin Walker", "Slenderman", "UFO", "Vampiro", "Wendigo", "Yeti"]

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


class Game(arcade.Window):
    """ Main application class. """

    def __init__(self, client):
        super().__init__(TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.client = client
        self.reset_position = False
        self.selected_card = None
        self.piles = None
        self.hand_size = 0
        self.has_selected = False
        self.client_cards = None
        self.flag_client_cards = False
        self.full_lobby = False
        self.text_log = "Que comece o jogo...\n"
        bg_text = arcade.load_texture("/home/sprites/button.png")
        
        # Create the UITextArea with initial text
        self.text_area = UITextArea(x=650, y=320, width=300, height=150, text=self.text_log)
        self.text_area_pane = UITexturePane(self.text_area.with_space_around(right=20),
                                            tex=bg_text, padding=(20, 20, 20, 20))
        self.manager.add(self.text_area_pane)



        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        tipo_button = arcade.gui.UIFlatButton(text="Tipo", width=200, height = 30)
        self.v_box.add(tipo_button.with_space_around(bottom=15))
        tipo_button.on_click = self.on_click_tipo

        tamanho_button = arcade.gui.UIFlatButton(text="Tamanho", width=200, height = 30)
        self.v_box.add(tamanho_button.with_space_around(bottom=15))
        tamanho_button.on_click = self.on_click_tamanho

        perigo_button = arcade.gui.UIFlatButton(text="Perigo", width=200, height = 30)
        self.v_box.add(perigo_button.with_space_around(bottom=15))
        perigo_button.on_click = self.on_click_perigo

        medo_button = arcade.gui.UIFlatButton(text="Medo", width=200, height = 30)
        self.v_box.add(medo_button.with_space_around(bottom=15))
        medo_button.on_click = self.on_click_medo

        avistamento_button = arcade.gui.UIFlatButton(text="Raridade", width=200, height = 30)
        self.v_box.add(avistamento_button.with_space_around(bottom=15))
        avistamento_button.on_click = self.on_click_avistamento
        
        avistamento_button = arcade.gui.UIFlatButton(text="Avistamento", width=200, height = 30)
        self.v_box.add(avistamento_button.with_space_around(bottom=15))
        avistamento_button.on_click = self.on_click_avistamento


        confirmar_button = arcade.gui.UIFlatButton(text="Escolher Carta", width=200, height = 40)
        confirmar_button.on_click = self.on_click_confirmar

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        self.background = arcade.load_texture("/home/sprites/game_screen.png")
        #arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

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

        self.p1.name = "test"

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
                align_y=-280,
                child=self.v_box)
        )

    def on_click_confirmar(self, event):
        print("enviar carta")
        self.hand_size -= 1
        if self.has_interacted_card and self.reset_position == False:
            self.has_selected = True
            data = {'header': 'play_card', 'request': {'name': self.selected_card.name} }
            self.client.sendMessage(data)
            #thread_receive.start()
            self.has_sent_message = True 
            self.has_interacted_card = False


    def on_click_tipo(self, event):
        self.text_log += "bap\n"
        print(self.text_log)
        print("tipo")
        inverted = self.revert_line_order(self.text_log)
        self.text_area.text = inverted

    def revert_line_order(self, input_string):
        lines = input_string.splitlines()
        reversed_lines = lines[::-1]
        result = '\n'.join(reversed_lines)
        return result
    
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
        threading.Thread(target=self.receive_message).start()
        time.sleep(2)
        #data = {'header': 'retrieve_deck', 'request': {}}
        #self.client.sendMessage(data)
        #draw_deck_cards = data

        #while True:
        #    if self.flag_client_cards:
        #        break

        #data = {'header': 'join_lobby', 'request': {'index': 0}}
        #self.client.sendMessage(data)

        self.held_cards = []
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.Sprite("/home/sprites/card_mat.png", scale=0.2)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the mats for the bottom face down and face up piles
        pile = arcade.Sprite("/home/sprites/hand.png", scale=0.2)
        pile.position = (START_X+ 630), BOTTOM_Y
        self.pile_mat_list.append(pile)

        #pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.color.DARK_OLIVE_GREEN)
        #pile.position = START_X + X_SPACING, BOTTOM_Y
        #self.pile_mat_list.append(pile)


        pile = arcade.Sprite("/home/sprites/card_mat.png", scale=0.2)
        pile.position = MIDDLE_SCREEN_X, (MIDDLE_SCREEN_Y + 120)
        self.pile_mat_list.append(pile)

        # pilha segundo jogador
        pile = arcade.Sprite("/home/sprites/card_mat.png", scale=0.2)
        pile.position = (MIDDLE_SCREEN_X/2), (MIDDLE_SCREEN_Y + 270)
        self.p2.mat = pile

        # pilha terceiro jogador
        pile = arcade.Sprite("/home/sprites/card_mat.png", scale=0.2)
        pile.position = (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X, (MIDDLE_SCREEN_Y + 270)
        self.p3.mat = pile

        pile = arcade.Sprite("/home/sprites/preview_card_mat.png", scale=0.35)
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
        size = len(self.piles[pile_index])
        print("size:", size)
        for card in self.piles[pile_index]:
            card.position = ((START_X+ 630) + 120 * (count)), BOTTOM_Y
            print("VALUE: ", (START_X+ 630) + 120 * (count))
            count += 1
        if size > 1: 
            for card in self.piles[pile_index]:
                card.position = card.center_x - 60, card.center_y   
            
    def centralize_hand_add(self, pile_index):
        size = len(self.piles[pile_index]) + 1
        if size == 1:
            print(size)
            for card in self.piles[pile_index]:
                card.position = (START_X+ 630), BOTTOM_Y     
        if size == 2:
            count = 0
            #for card in self.piles[pile_index]:
            #    card.position = ((START_X+ 510) + 60 * (count)), BOTTOM_Y
             #   count += 1
            for card in self.piles[pile_index]:
                card.position = card.center_x - 60, card.center_y         
        if size == 3:
            count = 0
            #for card in self.piles[pile_index]:
            #    card.position = ((START_X+ 510) + 60 * (count)), BOTTOM_Y
             #   count += 1
            for card in self.piles[pile_index]:
                card.position = card.center_x - 60, card.center_y    

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        self.p2.mat.draw()
        self.p3.mat.draw()

        # Draw the cards
        self.card_list.draw()

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
                        dropped_card.position = (top_card.center_x + 60 * (i + 1)), top_card.center_y
                        dropped_card.faceUp()
                        print(dropped_card.name)
                        self.hand_size += 1
                        self.centralize_hand_add(HAND)
                else:
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = pile.center_x, pile.center_y
                        dropped_card.faceUp()
                        print(dropped_card.name)
                        self.centralize_hand_add(HAND)
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

    def send_message(self, client_socket, message):
        data = {'message': message}
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

            
    def receive_message(self):
        while True:
            try:
                data_dict = self.client.receiveMessage()
                if data_dict['header'] == 'play_card':
                    print(data_dict['response']['card'])
                    self.render_opponent_card(data_dict['response']['card'])
            except Exception as e:
                print(str(e))
                break


    def render_opponent_card(self, message):
        for opponent in self.opponents:
            print(f"oponente name: {opponent.name}")
            print(message['player_name'])
            if opponent.name == message['player_name']:
                for card in self.card_list:
                    if card.name == message['card']:
                        opponent.card = arcade.Sprite(FACE_DOWN_IMAGE, CARD_SCALE)


def fabricateGame(client):
    player = input("insira o numero do jogador: ")
    deck = 1
    lobby = 0
    nome = ''
    senha = ''
    if player == '1':
        nome="bija"
        senha="bija123"
        pass
    elif player == '2':
        nome="patras"
        senha="patras123"
        pass
    elif player == '3':
        nome="thui"
        senha="thui123"
        pass
    
    msg1 = {'header': 'login', 'request': {'username': nome, 'password': senha}}
    msg2 = {'header': 'choose_deck', 'request': {'deck_id': deck}}
    msg3 = {'header': 'join_lobby', 'request': {'index': lobby}}
    msgs=[msg1, msg2, msg3]
    
    for i in range(3):
        data_str = json.dumps(msgs[i])
        try:
            client.s.sendall(bytes(data_str, encoding="utf-8"))
            time.sleep(3)
        except socket.error as e:
            print(str(e))
            client.s.close()

    if player==3:
        msg4 = {'header': 'start_game', 'request': {}}
        data_str = json.dumps(msg4)
        try:
            client.s.sendall(bytes(data_str, encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            client.s.close()
            
def receiveAnswer(client):
    while True:
        try:
            time.sleep(0.1)
            data = client.s.recv(1024)
            data_dict = json.loads(data.decode("utf-8"))
            print(data_dict)
        except socket.error as e:
            print(str(e))
            break

def main():

    client = Client()
    client.startClient()
    threading.Thread(target=receiveAnswer, args=(client,)).start()
    
    fabricateGame(client)
    
    window = Game(client)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
    
