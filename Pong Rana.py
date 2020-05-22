# We importeren arcade, omdat python zelf geen game kan ontwikkelen en arcade een soort van programma is die dat wel kan
import arcade
import time

# Hier geef je de waarden bij de constanten en de variabelen
# Constanten blijven constant (Hoofdletters) en variabelen kunnen veranderen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Pong"

# Hier geef je aan dat je muziek een volume heeft (maakt niet uit hoe hard het is)
MUSIC_VOLUME = 0.5

# Dit zijn 3 statussen
# State_Menu gebruik je als je in het menu bent
# State_Playing gebruik je als je speelt
# State_Game_Over gebruik je als je game over bent 
# De waarden die we hebben gegeven zijn nu nog niet nodig maar kunnen voor later wel handig zijn, 
# om sneller te kunnen verwijzen naar de game_state waar je in zit
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2


class scoreboard():

    # Dit zorgt ervoor dat de variabele 'bestaat'
    def __init__(self):
        self.position_x = None
        self.position_y = None
        self.font_side = None
        self.color = None
        self.score = None

    # In de setup geef je elke variabele een waarde. 
    def setup(self, position_x, position_y, font_side, color, score):

         self.position_x = position_x
         self.position_y = position_y
         self.font_side = font_side
         self.color = color
         self.score = score 

    # In de on_draw wordt alles getekend
    def on_draw(self):
         arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side, bold=True)

    # Hier wordt het tekenen van de score op het scoreboard telkens bijgewerkt
    def on_update(self):
         arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side, bold=True)


class ball():

    # Dit zorgt ervoor dat de variabele 'bestaat'
    def __init__(self):
     self.position_x = None
     self.position_y = None
     self.radius = None 
     self.color = None
     self.delta_x = None
     self.delta_y = None

    # In de setup geef je elke variabele een waarde. 
    def setup(self, position_x, position_y, radius, color, delta_x, delta_y):
     self.position_x = position_x
     self.position_y = position_y
     self.radius = radius 
     self.color = color
     self.delta_x = delta_x 
     self.delta_y = delta_y

    # In de on_draw wordt alles getekend
    def on_draw(self):
         arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    # delta_time is de verstreken tijd tussen twee updates, hiermee kun je dingen evenredig door de tijd heen bewegen 
    # Om de bal te laten bewegen moet hij gelijk staan aan zijn eigen positie + de verandering
    def  on_update(self, delta_time, paddle_a, paddle_b, score_board, score_board2):
         self.position_x = self.position_x + self.delta_x
         self.position_y = self.position_y + self.delta_y

    # Als de bal de boven- of onderkant van het scherm raakt moet hij terug en niet uit het scherm
    # Hiervoor doen we de richting * -1, zodat hij de negatieve (dus in het scherm) kant op gaat
    # Voor de onderrand heb ik y = 70 gebruikt, omdat dit de straal van de bal is
    # Hierdoor gaat geen enkel deel van de bal uit het scherm
         if self.position_y + self.radius >= SCREEN_HEIGHT: 
             self.delta_y = self.delta_y * -1 
         if self.position_y + self.radius <= 50:
             self.delta_y = self.delta_y * -1

    # Hier wordt aangegeven dat als de bal de de paddle raakt niet er doorheen gaat maar terug wordt gekaatst 
         if self.position_x + self.radius >= paddle_a.position_x - paddle_a.width // 2 and \
            self.position_x - self.radius <= paddle_a.position_x + paddle_a.width // 2 and \
            self.position_y + self.radius >= paddle_a.position_y - paddle_a.height // 2 and \
            self.position_y - self.radius <= paddle_a.position_y + paddle_a.height // 2:
            self.delta_x *= -1

    # Hier wordt aangegeven dat als de bal de de paddle raakt niet er doorheen gaat maar terug wordt geschoten 
         if self.position_x + self.radius >= paddle_b.position_x - paddle_b.width // 2 and \
            self.position_x - self.radius <= paddle_b.position_x + paddle_b.width // 2 and \
            self.position_y + self.radius >= paddle_b.position_y - paddle_b.height // 2 and \
            self.position_y - self.radius <= paddle_b.position_y + paddle_b.height // 2:
            self.delta_x *= -1

    # In deze twee groepen wordt er aangegeven dat als er wordt gescoord, 
    # de bal weer in het midden gespawned moet worden en de tegengestelde richting op moet gaan
    # Ook wordt er aangegeven dat als er wordt gescoort er een punt bij het scorebord moet worden opgeteld
         if self.position_x >= 1000:
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1
                score_board.score += 1
            
         if self.position_x <= 0:
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1
                score_board2.score += 1


class rectangle():

    # Dit zorgt ervoor dat de variabele 'bestaat'
    # We gebruiken hier self.change ipv self.delta, omdat we ook daadwerkelijk de paddles moeten verschuiven
    # We laten ze 'changen' van plek (ook is er geen tijd dus hebben we delta niet nodig)
    def __init__(self):         
         self.position_x = None
         self.position_y = None 
         self.width = None
         self.height = None
         self.color = None
         self.tilt_angle = None 
         self.change_y = None
         self.change_x = None

    # In de setup geef je elke variabele een waarde. 
    def setup(self, position_x, position_y, width, height, color, change_y, change_x):
         self.position_x = position_x
         self.position_y = position_y
         self.width = width
         self.height = height 
         self.color = color
         self.change_y = change_y
         self.change_x = change_x


    # In de on_draw wordt alles getekend
    def on_draw(self):
         arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color,)

    # Hier wordt telkens de plaats van de paddle bijwerken
    def on_update(self, delta_time):
        self.position_y += self.change_y * delta_time
        self.position_x += self.change_x * delta_time
        
        # Hier zorg je ervoor dat de paddles niet door de boven- of onderkant uit het scherm schuiven,
        # maar stoppen met bewegen
        if self.position_y < self.height/2:
             self.position_y = self.height/2
        if self.position_y > SCREEN_HEIGHT - self.height/2:
             self.position_y = SCREEN_HEIGHT - self.height/2


class MyGame(arcade.Window):
    def __init__(self, width, height, title):

        # Super geeft de waarden door aan het arcade venster die alles uitvoert
         super().__init__(width, height, title)

        # Hier zorg je ervoor dat je de muis wel of niet ziet in het scherm, in dit geval NIET
         self.set_mouse_visible(False)

        # Hier stel je de kleur van het venster in, je gebruikt arcade om een lijst met kleuren 'op te vragen'
         arcade.set_background_color(arcade.color.BLUEBERRY)

         self.ball = None 
         self.rectangle = None
         self.rectangle2 = None
         self.paddlespeed = 450
         self.score_board = None
         self.score_board2 = None

        # In de self.game_state wordt er aangegeven in welke status je zit (nu nog niet)
         self.game_state = None

        # Hier maak je een muziek lijst en een nummer die wordt afgespeeld, maar nu hebben ze nog geen waarden
         self.music_list = []
         self.current_song = 0
         self.music = None

    # Hier Speel je het liedje af
    def play_song(self):
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)

    # In de setup van MyGame worden alle waarden van de classses aangegeven
    # Als je iets wilt aanpassen aan bijv. de snelheid van de bal of de kleur van de paddle,
    # dan doe je dat in de setup van MyGame
    def setup(self):
         self.music_list = ["Pong Music.mp3"]
         self.current_song = 0
         self.play_song()

         self.ball = ball()
         self.ball.setup(500, 350, 25, arcade.color.WHITE, 12, 12)

         self.rectangle = rectangle()
         self.rectangle.setup(50, 350, 50, 200, arcade.color.WHITE, 0, 0)

         self.rectangle2 = rectangle()
         self.rectangle2.setup(950, 350, 50, 200, arcade.color.WHITE, 0, 0)

         self.score_board = scoreboard()
         self.score_board.setup(260, 600, 40, arcade.color.LIGHT_GRAY, 0)
        
         self.score_board2 = scoreboard()
         self.score_board2.setup(540, 600, 40, arcade.color.LIGHT_GRAY, 0)

        # Hier geef je aan dat je in GAME_STATE_MENU zit (boven is de waarde van MENU = 0)
         self.game_state = 0

    # Op het moment dat je begint met start_render tekent hij alles, dit hoeft maar één keer,
    # en het hoeft ook niet gestopt te worden
    def on_draw(self):
         arcade.start_render()
         if self.game_state == STATE_PLAYING:
             point_list = ((SCREEN_WIDTH//2, 693),
              (SCREEN_WIDTH//2, 665),
              (SCREEN_WIDTH//2, 651),
              (SCREEN_WIDTH//2, 623),
              (SCREEN_WIDTH//2, 609),
              (SCREEN_WIDTH//2, 581),
              (SCREEN_WIDTH//2, 567),
              (SCREEN_WIDTH//2, 539),
              (SCREEN_WIDTH//2, 525),
              (SCREEN_WIDTH//2, 497),
              (SCREEN_WIDTH//2, 483),
              (SCREEN_WIDTH//2, 455),
              (SCREEN_WIDTH//2, 441),
              (SCREEN_WIDTH//2, 413),
              (SCREEN_WIDTH//2, 399),
              (SCREEN_WIDTH//2, 371),
              (SCREEN_WIDTH//2, 357),
              (SCREEN_WIDTH//2, 329),
              (SCREEN_WIDTH//2, 315),
              (SCREEN_WIDTH//2, 287),
              (SCREEN_WIDTH//2, 273),
              (SCREEN_WIDTH//2, 245),
              (SCREEN_WIDTH//2, 234),
              (SCREEN_WIDTH//2, 206),
              (SCREEN_WIDTH//2, 192),
              (SCREEN_WIDTH//2, 164),
              (SCREEN_WIDTH//2, 150),
              (SCREEN_WIDTH//2, 122),
              (SCREEN_WIDTH//2, 108),
              (SCREEN_WIDTH//2, 80),
              (SCREEN_WIDTH//2, 66),
              (SCREEN_WIDTH//2, 38),
              (SCREEN_WIDTH//2, 24),
              (SCREEN_WIDTH//2, 0))
             arcade.draw_points(point_list, arcade.color.LIGHT_GRAY, 14)
             self.ball.on_draw()
             self.rectangle.on_draw()
             self.rectangle2.on_draw()
             self.score_board.on_draw()
             self.score_board2.on_draw()

        # Hier geef je aan wat hij moet typen als je GAME OVER bent
         if self.game_state == STATE_GAME_OVER:
             arcade.draw_text(f" GAME OVER" , 155, 300, arcade.color.WHITE, 100, bold=True,)
             arcade.draw_text(f" (PRESS ENTER TO PLAY AGAIN)" , 345, 80, arcade.color.RED, 20, bold=True)

        # Hier geef je aan wat hij moet typen als je gaat beginnen met het spel
         if self.game_state == STATE_MENU:
             arcade.draw_text(f" PRESS SPACE TO START" , 10, 300, arcade.color.WHITE, 80, bold=True)

            

    # Hier update hij telkens de positie van alle variabele die erin staan
    def on_update(self, delta_time):
        if self.game_state == STATE_PLAYING: 
             self.ball.on_update(delta_time, self.rectangle, self.rectangle2, self.score_board, self.score_board2)
             self.rectangle.on_update(delta_time)
             self.rectangle2.on_update(delta_time)
             self.score_board.on_update()
             self.score_board2.on_update()

        # Hier geef je aan dat het spel eindigt als iemand 3 punten heeft gescoord, dan ga je dus naar STATE_GAME_OVER
        if self.score_board.score == 3 or self.score_board2.score == 3:
                 self.game_state = STATE_GAME_OVER

        if self.game_state == STATE_MENU:
             pass


    def on_key_press(self, key, key_modifiers):
        if self.game_state == STATE_PLAYING:
            if key == arcade.key.UP:
                self.rectangle2.change_y = self.paddlespeed
            elif key == arcade.key.DOWN:
                self.rectangle2.change_y = -self.paddlespeed

            if key == arcade.key.W:
                self.rectangle.change_y = self.paddlespeed
            elif key == arcade.key.S:
                self.rectangle.change_y = -self.paddlespeed

        # Hier geef je aan dat als je op spatie klikt de game start
        # en als je op enter klikt de game kan restarten, 
        # LET OP dit kan alleen als het spel al is afgelopen, dus als je game over bent
        if self.game_state == STATE_MENU:
            if key == arcade.key.SPACE:
                self.game_state = STATE_PLAYING

        if self.game_state == STATE_GAME_OVER:
            if key == arcade.key.ENTER:
                self.game_state = STATE_MENU
                # Hier reset je de score, omdat je begint aan een nieuw potje
                self.score_board.score = 0
                self.score_board2.score = 0

    # Hier geef je aan dat als je de key loslaat, de paddles moeten stoppen met bewegen 
    # en niet doorgaan met verplaatsen totdat je ze naar een andere richting stuurt
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rectangle2.change_y = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.rectangle.change_y = 0

# De main functie is het startpunt van het programma            
def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    # Arcade run zorgt ervoor dat alles op gang wordt gezet


if __name__ == "__main__":
    main()

