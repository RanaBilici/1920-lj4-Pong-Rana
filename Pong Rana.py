# We importeren arcade, omdat python zelf geen game kan ontwikkelen en arcade een soort programma is die dat wel kan
import arcade

# Hier geef je de waarden bij de constanten en de variabelen
# Constanten blijven constant (Hoofdletters) en variabelen kunnen veranderen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Pong"

# Dit zijn 3 statussen
# State_Menu gebruik je als je in het menu bent
# State_Playing gebruik je als je speelt
# State_Game_Over gebruik je als je game over bent 
# Dewaardes die we hebben gegeven zijn nu nog niet nodig maar kunnen voor later wel andig zijn
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2


class scoreboard():

    def __init__(self):
        self.position_x = None
        self.position_y = None
        self.font_side = None
        self.color = None
        self.score = None


    # In de setup geef je elke self. een waarde. Dit zorgt ervoor dar de self. 'bestaat'
    def setup(self, position_x, position_y, font_side, color, score):

         self.position_x = position_x
         self.position_y = position_y
         self.font_side = font_side
         self.color = color
         self.score = score 


    # In de on_draw wordt alles getekend
    def on_draw(self):
         arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side)

    def on_update(self):
         arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side)


class ball():

    def __init__(self):
     self.position_x = None
     self.position_y = None
     self.radius = None 
     self.color = None
     self.delta_x = None
     self.delta_y = None


    # In de setup geef je elke self. een waarde. Dit zorgt ervoor dar de self. 'bestaat'
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
    # Voor nu is het niet perse nodig, maar als je er later wel wat mee wilt doen is het handig dat het erbij staat
    # Om de bal te laten bewegen moet hij gelijk staan aan zijn eigen positie + de verandering
    def  on_update(self, delta_time, paddle_a, paddle_b, score_board, score_board2):
         self.position_x = self.position_x + self.delta_x
         self.position_y = self.position_y + self.delta_y

    # Als de bal de rand van het scherm raakt moet hij terug en niet uit het scherm
    # Hiervoor doen we de richting * -1, zodat hij de negatieve richting op gaat
    # Voor de onderrand heb ik y = 70 gebruikt, omdat dit de straal van de bal is
    # Hierdoor gaat geen enkel deel van de bal uit het scherm
         if self.position_y + self.radius >= SCREEN_HEIGHT: 
             self.delta_y = self.delta_y * -1 
         
         if self.position_y + self.radius <= 70:
             self.delta_y = self.delta_y * -1

        
         if self.position_x + self.radius >= paddle_a.position_x - paddle_a.width // 2 and \
            self.position_x - self.radius <= paddle_a.position_x + paddle_a.width // 2 and \
            self.position_y + self.radius >= paddle_a.position_y - paddle_a.height // 2 and \
            self.position_y - self.radius <= paddle_a.position_y + paddle_a.height // 2:
            self.delta_x *= -1

         if self.position_x + self.radius >= paddle_b.position_x - paddle_b.width // 2 and \
            self.position_x - self.radius <= paddle_b.position_x + paddle_b.width // 2 and \
            self.position_y + self.radius >= paddle_b.position_y - paddle_b.height // 2 and \
            self.position_y - self.radius <= paddle_b.position_y + paddle_b.height // 2:
            self.delta_x *= -1


         if self.position_x >= 1000:
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1
                score_board.score += 1
            
         if self.position_x <= 0:
                score_board2.score += 1
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1


class rectangle():

    # We gebruiken hier self.change ipv self.delta, omdat we ook daadwerkelijk de paddles moeten verschuiven
    # We laten ze 'changen' van plek
    def __init__(self):         
         self.position_x = None
         self.position_y = None 
         self.width = None
         self.height = None
         self.color = None
         self.tilt_angle = None 
         self.change_y = None
         self.change_x = None


    # In de setup geef je elke self. een waarde. Dit zorgt ervoor dar de self. 'bestaat'
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


    def on_update(self, delta_time):
        self.position_y += self.change_y * delta_time
        self.position_x += self.change_x * delta_time
        
        # Hier zorg je ervoor dat de paddles de boven- en onderkant van het scherm niet raken
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
         self.paddlespeed = 400
         self.score_board = None
         self.score_board2 = None
         self.game_state = None
         # Hier geef je aan in welke status je zit

    def setup(self):
         self.ball = ball()
         self.ball.setup(500, 350, 35, arcade.color.WHITE, 8, 8)

         self.rectangle = rectangle()
         self.rectangle.setup(50, 350, 55, 200, arcade.color.WHITE, 0, 0)

         self.rectangle2 = rectangle()
         self.rectangle2.setup(950, 350, 55, 200, arcade.color.WHITE, 0, 0)

         self.score_board = scoreboard()
         self.score_board.setup(260, 600, 40, arcade.color.WHITE, 0)
        
         self.score_board2 = scoreboard()
         self.score_board2.setup(540, 600, 40, arcade.color.WHITE, 0)

         self.game_state = 0

    # Op het moment dat je begint met start_render tekent hij alles, dit hoeft maar een keer
    def on_draw(self):
         arcade.start_render()
         if self.game_state == STATE_PLAYING:
             self.ball.on_draw()
             self.rectangle.on_draw()
             self.rectangle2.on_draw()
             self.score_board.on_draw()
             self.score_board2.on_draw()

         if self.game_state == STATE_GAME_OVER:
             arcade.draw_text(f" GAME OVER" , 155, 300, arcade.color.WHITE, 100, bold=True)

         if self.game_state == STATE_MENU:
             arcade.draw_text(f" PRESS SPACE TO START" , 10, 300, arcade.color.WHITE, 80, bold=True)

            

    # Hier update hij telkens de positie alle waardes die erin staan
    def on_update(self, delta_time):
        if self.game_state == STATE_PLAYING: 
             self.ball.on_update(delta_time, self.rectangle, self.rectangle2, self.score_board, self.score_board2)
             self.rectangle.on_update(delta_time)
             self.rectangle2.on_update(delta_time)
             self.score_board.on_update()
             self.score_board2.on_update()

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
        # ! voor de "=" betekent niet 
        # Dit gebruik je omdat je niet midden in het spel het spel weer opnieuw wilt starten,
        # maar alleen als je gaat beginnen met het spelen

        if self.game_state == STATE_MENU:
            if key == arcade.key.SPACE:
                self.game_state = STATE_PLAYING

        if self.game_state == STATE_GAME_OVER:
            if key == arcade.key.ENTER:
                self.game_state = STATE_MENU

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rectangle2.change_y = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.rectangle.change_y = 0

            
def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    # Arcade run zorgt ervoor dat alle vensters worden 'getekend' als het ware


if __name__ == "__main__":
    main()