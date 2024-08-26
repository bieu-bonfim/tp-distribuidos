import arcade
import random
import socket
import threading
import time
import json
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import win_screen
import Pyro5.api

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

FACE_DOWN_IMAGE = "/home/cards/backcard.jpg"

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
        self.image_file_name = f"/home/cards/{name}.jpg"
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

    def __init__(self, name, card, mat):
        self.name = name
        self.card = card
        self.mat = mat


class Game(arcade.View):
    """ Main application class. """

    def __init__(self, session, op1, op2, turn_order, game_server, index, player_deck_cards):
        super().__init__()
        self.turn_order = turn_order
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.lobby_index = index
        self.session = session
        self.game_server_backup = game_server
        self.game_server = Pyro5.api.Proxy(game_server._pyroUri)
        self.client = self.game_server.get_client(self.session)
        self.reset_position = False
        self.selected_card = None
        self.piles = None
        self.hand_size = 0
        self.has_selected = False
        self.client_cards = player_deck_cards
        self.flag_client_cards = False
        self.full_lobby = False
        self.text_log = "Boas vindas a Cryptids...\n"
        bg_text = arcade.load_texture("/home/sprites/text_area.png")
        self.have_put_play = False
        self.is_turn_now = False
        self.actual_turn = 1
        self.select_name_turn = 0
        self.turn_name = turn_order[0]
        self.text_area = UITextArea(x=650, y=320, width=300, height=150, text=self.text_log)
        self.text_area_pane = UITexturePane(self.text_area.with_space_around(right=20),
                                            tex=bg_text, padding=(20, 20, 20, 20))
        self.manager.add(self.text_area_pane)
        self.game_proxy = None
        self.winner_setted = False

        # winner logic -----------
        self.is_draw = False
        self.resolve_turn = False
        self.turn_winner = None
        self.end_game = False
        self.winner_name = None
        # ----------------------

        self.has_new_log = False

        self.is_turn_over_time = False

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

        raridade = arcade.gui.UIFlatButton(text="Raridade", width=200, height = 30)
        self.v_box.add(raridade.with_space_around(bottom=15))
        raridade.on_click = self.on_click_raridade
        
        avistamento_button = arcade.gui.UIFlatButton(text="Avistamento", width=200, height = 30)
        self.v_box.add(avistamento_button.with_space_around(bottom=15))
        avistamento_button.on_click = self.on_click_avistamento


        confirmar_button = arcade.gui.UIFlatButton(text="Escolher Carta", width=200, height = 40)
        confirmar_button.on_click = self.on_click_confirmar


        self.card_list = None
        self.background = arcade.load_texture("/home/sprites/game_screen.png")
        self.held_cards = None
        self.opponents = []
        self.held_cards_original_position = None
        self.pile_mat_list = None

        self.p1 = Player(name=self.client.get_username(), card=None, mat=None)
        self.p2 = Player(name=op1, card=None, mat=None)
        self.p3 = Player(name=op2, card=None, mat=None)

        self.opponents.append(self.p2)
        self.opponents.append(self.p3)

        self.p1.name = self.client.get_username()

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

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_x=510,
                align_y=-280,
                child=self.v_box)
        )

    def on_click_confirmar(self, event):
        if self.selected_card != None:
            print("enviar carta")
            self.hand_size -= 1
            _, self.is_turn_over_time = self.game_proxy.play_card(self.selected_card.name, self.client)
            self.add_log(f"Você escolheu {self.selected_card.name}...\n")
            self.winner_setted = False
        else:
            print("Escolha uma carta")
            self.winner_setted = False

    def add_log(self, new_log):
        self.text_log += new_log
        inverted = self.revert_line_order(self.text_log)
        self.text_area.text = inverted

    def revert_line_order(self, input_string):
        lines = input_string.splitlines()
        reversed_lines = lines[::-1]
        result = '\n'.join(reversed_lines)
        return result
    
    def on_click_tipo(self, event):
        self.game_proxy.choose_stat('Tipo', self.client)
        self.winner_setted = False
        print("tipo")
        self.add_log(f"Atributo Tipo escolhido...\n")
    
    def on_click_tamanho(self, event):
        self.game_proxy.choose_stat('Tamanho', self.client)
        self.winner_setted = False
        print("tamanho")
        self.add_log(f"Atributo Tamanho escolhido...\n")

    def on_click_perigo(self, event):
        self.game_proxy.choose_stat('Perigo', self.client)
        self.winner_setted = False
        print("perigo")
        self.add_log(f"Atributo Perigo escolhido...\n")

    def on_click_medo(self, event):
        self.game_proxy.choose_stat('Medo', self.client)
        self.winner_setted = False
        print("medo")
        self.add_log(f"Atributo Medo escolhido...\n")

    def on_click_raridade(self, event):
        self.game_proxy.choose_stat('Raridade', self.client)
        self.winner_setted = False
        print("raridade")
        self.add_log(f"Atributo Raridade escolhido...\n")

    def on_click_avistamento(self, event):
        self.game_proxy.choose_stat('Avistamento', self.client)
        self.winner_setted = False
        print("avistamento")

    
    def setup(self):
        print("--------- ORDEM DO TURNO ------- ", self.turn_order)
        print(self.p2.name)
        print(self.p3.name)

        self.held_cards = []
        self.held_cards_original_position = []

        # --- Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        pile = arcade.Sprite("/home/sprites/card_mat.png", scale=0.2)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)
        pile = arcade.Sprite("/home/sprites/hand.png", scale=0.2)
        pile.position = (START_X+ 630), BOTTOM_Y
        self.pile_mat_list.append(pile)

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
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_name in self.client_cards:
            card = Card(card_name, CARD_SCALE)
            card.position = START_X, BOTTOM_Y
            self.card_list.append(card)


        
        self.piles = [[] for _ in range(PILE_COUNT)]

        for card in self.card_list:
            self.piles[DRAW].append(card)

        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        self.game_proxy = Pyro5.api.Proxy(self.game_server._pyroUri)

        self.add_log(f"O turno é de {self.turn_name}...\n")

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
            for card in self.piles[pile_index]:
                card.position = card.center_x - 60, card.center_y         
        if size == 3:
            count = 0
            for card in self.piles[pile_index]:
                card.position = card.center_x - 60, card.center_y    

    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.game_logic()

        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        self.pile_mat_list.draw()
        self.p2.mat.draw()
        self.p3.mat.draw()

        self.card_list.draw()

        arcade.draw_text(
            self.p1.name,
            start_x= MIDDLE_SCREEN_X/2 + 30,
            start_y= MIDDLE_SCREEN_Y -200,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Turno Atual: "+ str(self.actual_turn),
            start_x= MIDDLE_SCREEN_X/2 + 70,
            start_y= MIDDLE_SCREEN_Y -240,
            color=arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Escolhendo agora: "+ str(self.turn_order[self.select_name_turn]),
            start_x= MIDDLE_SCREEN_X/2 + 70,
            start_y= MIDDLE_SCREEN_Y -270,
            color=arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            anchor_y="center"
        )


        arcade.draw_text(
            "Cartas no deck: "+ str(len(self.piles[DRAW])),
            start_x= START_X,
            start_y= TOP_Y -370,
            color=arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            anchor_y="center"
        )


        if self.current_hovered_card:
            amplified_card = arcade.Sprite(self.current_hovered_card.image_file_name, SHOWCASE_CARD_SCALE)
            amplified_card.position = END_X, TOP_Y_SHOWCASE
            amplified_card.draw()

        arcade.draw_text(
            self.p2.name,
            start_x= (MIDDLE_SCREEN_X/2) - 140,
            start_y= (MIDDLE_SCREEN_Y + 340),
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center")

        arcade.draw_text(
            self.p3.name,
            start_x= (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X + 140,
            start_y= (MIDDLE_SCREEN_Y + 340),
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center")

        if self.p2.card != None:
            self.p2.card.position = (MIDDLE_SCREEN_X/2), (MIDDLE_SCREEN_Y + 270)
            self.p2.card.draw()

        if self.p3.card != None:
            self.p3.card.position = (MIDDLE_SCREEN_X/2)+MIDDLE_SCREEN_X, MIDDLE_SCREEN_Y + 270
            self.p3.card.draw()


        if self.has_new_log:
            inverted = self.revert_line_order(self.text_log)
            self.text_area.text = inverted
            self.has_new_log = False

        if self.is_turn_over_time:
            for opponent in self.opponents:
                opponent.card.faceUp()
            self.is_turn_over_time = False

        if self.resolve_turn:
            self.resolve_turn = False
            if self.is_draw:
                print('EMPATE')
                self.is_draw = False
                self.selected_card.faceDown()
                self.selected_card = START_X, BOTTOM_Y
                self.move_card_to_new_pile(self.selected_card, DRAW)
                self.selected_card = None
                for pos1 in range(len(self.card_list)):
                    pos2 = random.randrange(len(self.card_list))
                    self.card_list.swap(pos1, pos2)
                self.have_put_play = False

            elif self.turn_winner == self.client.get_username():
                print(' Ganhou ')
                for opponent in self.opponents:
                    if opponent.card != None:
                        opponent.card.faceDown()
                        opponent.card.position = START_X, BOTTOM_Y
                        self.move_card_to_new_pile(opponent.card, DRAW)
                        self.card_list.append(opponent.card)
                        opponent.card = None
                if self.selected_card != None:
                    self.selected_card.faceDown()
                    self.selected_card.position = START_X, BOTTOM_Y
                    self.move_card_to_new_pile(self.selected_card, DRAW)
                    self.selected_card = None

                self.turn_winner = None
                self.have_put_play = False

                for pos1 in range(len(self.card_list)):
                    pos2 = random.randrange(len(self.card_list))
                    self.card_list.swap(pos1, pos2)


            else:
                print("CARD = ", self.selected_card.name)
                if self.have_put_play:
                    self.card_list.remove(self.selected_card)
                    self.have_put_play = False
                for opponent in self.opponents:
                    opponent.card = None
                print(" PERDEU ")



            self.actual_turn += 1

        if self.end_game:
            win = win_screen.WinScreen(self.session, self.game_server_backup, self.winner_name)
            self.window.show_view(win)



    def on_mouse_press(self, x, y, button, key_modifiers):
        self.has_interacted_card = True
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        if len(cards) > 0:
            primary_card = cards[-1]
            self.held_cards = [primary_card]
            self.held_cards_original_position = [self.held_cards[0].position]
            self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):


        if len(self.held_cards) == 0:
            return

        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        self.reset_position = True

        if arcade.check_for_collision(self.held_cards[0], pile):

            pile_index = self.pile_mat_list.index(pile)

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
                self.have_put_play = True
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

        self.handle_hover(x, y)

    def handle_hover(self, x, y):
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        if len(cards) > 0:
            hovered_card = cards[-1]

            # Check if this card is already hovered
            if self.last_hovered_card != hovered_card:
                if self.last_hovered_card is not None:
                    self.last_hovered_card.alpha = 255
                self.last_hovered_card = hovered_card

            if hovered_card.isFaceUp() == True:
                self.current_hovered_card = hovered_card

        else:
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

    def render_opponent_card(self, card_name, player_name):
        for opponent in self.opponents:
            if opponent.name == player_name:
                for card in CARD_NAMES:
                    if card == card_name:
                        #opponent.card = arcade.Sprite(FACE_DOWN_IMAGE, CARD_SCALE)
                        op_card = Card(card, CARD_SCALE)
                        opponent.card = op_card


    def game_logic(self):
        moment_winner = self.game_proxy.get_winner(self.client)
        if  moment_winner != "" and self.winner_setted == False:
                self.winner_setted = True
                self.add_log(f"O vencedor do turno é {moment_winner}...\n")
                self.turn_winner = moment_winner
                self.resolve_turn = True
                if self.select_name_turn < 3 and self.actual_turn < 3:
                    self.select_name_turn += 1
                else:
                    self.select_name_turn = 0
        elif moment_winner == "draw":
            self.is_draw = True
            self.resolve_turn = True
        player_names, played_cards  = self.game_proxy.get_played_cards(self.client)
        for i in range(len(player_names)):
            if player_names[i] == self.p1.name:
                continue
            if player_names[i] == self.p2.name:
                self.render_opponent_card(played_cards[i], self.p2.name)
            if player_names[i] == self.p3.name:
                self.render_opponent_card(played_cards[i], self.p3.name)

        if played_cards.count(None) == 0:
            self.is_turn_over_time = True

        end_game_winner = self.game_proxy.get_game_winner(self.client)
        if end_game_winner != "":
            self.winner_name = end_game_winner
            self.end_game = True


