# GAME TITLE: VAMPIRE TERROR
# CREATED AND DEVELOPED BY KELOMPOK A - KELAS C - INDONESIAN WOMEN IN TECH
# YEAR: 2021

###### MODULS & LIBRARIES #######
import pygame
pygame.init()
import pandas as pd #for bank data management
import random #for randomizing the Q&A
import pyttsx3 #for voiceing the call a friend
from pygame import mixer #for setting the backsound musics and sound effects

##### LOADING THE OPENING MUSIC AND CREATING THE SCREEN
mixer.music.load('musicNsound/bensound-creepy.mp3')
mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.4)
screen = pygame.display.set_mode((1352,652))

#### CLOCK
clock = pygame.time.Clock()
fps = 60

#### SET THE FONTS
font = pygame.font.SysFont('KRONIKA_.ttf', 23)
fontset = pygame.font.Font('KRONIKA_.ttf',22)

##### SETTING THE GAME TITLE & ICON
pygame.display.set_caption("Vampire Terror")
icon = pygame.image.load('png/vampire.png')
pygame.display.set_icon(icon)

#### LOADING THE GAME LOGO
openingLogo = pygame.image.load('png/logogame.png')
screen.blit(openingLogo,(0,0))
pygame.display.update()
pygame.time.delay(2000) #Played for 2 seconds

#### LOADING IMAGES FOR OPENING STORY SCENE
openingImage = pygame.image.load('png/backgroundintro.png')
daytime = pygame.image.load('png/basicsiang.png')
nighttime = pygame.image.load('png/basicmalam.png')
textboxIntro = pygame.image.load('png/textboxintro.png')
closingbg = pygame.image.load('png/closing.png')

#### LOADING THE QUESTION BANK
data = pd.read_csv("https://raw.githubusercontent.com/umiseldaa/finalproject/main/question%20bank.csv",sep=',')
data.head()
questions = data.Q.to_list()
print(questions)
corrects = data.C.to_list()
print(corrects)
answers = data.filter(like="Alter") #Select the columns only containing A,B,C,D option answers
answers = answers.values.tolist()

# shuffling ABCD options
for i in range(len(answers)):
    random.shuffle(answers[i])

# shuffling all questions & answers
Q = questions
A = answers
C = corrects
qa = list(zip(Q, A, C)) # this is to compile questions, answer options and correct answer
random.shuffle(qa)
Q, A, C = zip(*qa)
print(qa[0])

#### SETTING UP THE SKY BACKGROUND
cloud_front = pygame.image.load('png/awandepan.png')
cloud_back = pygame.image.load('png/awanbelakang.png')
moon = pygame.image.load('png/bulan.png')

#### SETTING UP THE BUTTONS
class Button:
    def __init__(self,text,width,height,pos,elevation):
		# Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

		# top rectangle
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#fcaa3d'

		# bottom rectangle
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#9b5901'

		#text
        self.text_surf = fontset.render(text,True,'#000000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
		# elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print("self")
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#fcaa3d'

    def disable_button(self):
        self.pressed = False
        self.top_color = '#7F7F7F'

		# bottom rectangle
        self.bottom_color = '#515151'

##### SETTING UP THE BUTTON THAT IS USING IMAGE (FOR HELP BUTTONS)
class help_button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def put(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

    def disable_button(self):
        self.pressed = False
        #self.top_color = '#7F7F7F'

#### SETTING UP THE VAMPIRE'S MOVE
def vampire_move(vamx, vamy):
    gameDisplay.blit(vampireImage, (vamx, vamy))

#### LOADING THE VAMPIRE IMAGE AND SETTING UP THE POSITION
vampireImage = pygame.image.load('png/Vampire1.png')
vamx = 950  # position vampire
vamy = 150 # position vampire

#### SETTING UP THE GARLIC BULLET
# Ready: garlic appear on screen
# Fire: garlic is moving
garlic = pygame.image.load("png/garlic.png")

def garlic_shoot(x,y):
    global garlic_state
    garlic_state = "fire"
    screen.blit(garlic,(x, y))

##### LOADING THE HELP BUTTONS (USING IMAGES)
button_50 = pygame.image.load('png/5050.png')
button_callafriend = pygame.image.load('png/callafriend.png')
button_golden = pygame.image.load('png/goldenbutton.png')

button_50off = pygame.image.load('png/5050off.png')
button_callafriendoff = pygame.image.load('png/callafriendoff.png')
button_goldenoff = pygame.image.load('png/goldenbuttonoff.png')

#### CREATING THE AREA AND BUTTONS FOR Q&A
questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
tryagain = Button("Try Again", 300, 40, (550, 320), 5)
start = Button("Start", 300, 40, (510, 400), 5)
quit_button = Button("Quit", 300, 40, (550, 385), 5)

#### BASIC SCORE & LIFE SETTING
Score = 0
life = 3
inputAnswer =[]
notif =""

#### LOADING THE PLAYER'S LIFE ICON
lifeIconON1 = pygame.image.load('png/nyawa.png')
lifeIconOFF1 = pygame.image.load('png/nyawaoff.png')

lifeIconON2 = pygame.image.load('png/nyawa.png')
lifeIconOFF2 = pygame.image.load('png/nyawaoff.png')

lifeIconON3 = pygame.image.load('png/nyawa.png')
lifeIconOFF3 = pygame.image.load('png/nyawaoff.png')

#### LOADING THE IMAGES FOR VAMPIRE'S LIFE ICON / SCORE DETECTION
vampirelife0 = pygame.image.load('png/nyawa0.png')
vampirelife1 = pygame.image.load('png/nyawa1.png')
vampirelife2 = pygame.image.load('png/nyawa2.png')
vampirelife3 = pygame.image.load('png/nyawa3.png')
vampirelife4 = pygame.image.load('png/nyawa4.png')
vampirelife5 = pygame.image.load('png/nyawa5.png')
vampirelife6 = pygame.image.load('png/nyawa6.png')
vampirelife7 = pygame.image.load('png/nyawa7.png')
vampirelife8 = pygame.image.load('png/nyawa8.png')
vampirelife9 = pygame.image.load('png/nyawa9.png')
vampirelife10 = pygame.image.load('png/nyawa10.png')
dashboard = pygame.image.load('png/nyawaboard.png')

#### LOADING IMAGES FOR THE OPENING STORY SCENE
bgdialogue = pygame.image.load('png/basicmalam.png')
dial_1 = pygame.image.load('png/d1.png')
ballon_1 = pygame.image.load('png/convo1.png')
dial_2 = pygame.image.load('png/d2.png')
ballon_2 = pygame.image.load('png/convo1.png')
dial_3 = pygame.image.load('png/d3.png')
ballon_3 = pygame.image.load('png/convo.png')

###++++++++++++++++++++++++++++ CORE PROCESS +++++++++++++++++++++++++++++###

####### OPENING STORY
def opening_story():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            # Press any key to go to the next scene.
            elif event.type ==pygame.KEYDOWN:
                return dialogue_1

        screen.fill('#D74B4B')
        screen.blit(openingImage, (0, 0))
        screen.blit(textboxIntro, (0, 0))
        openingStory1 = font.render('Di pelosok negeri ini, ada sebuah desa', True,
                                    "Black")
        screen.blit(openingStory1, (520, 230))
        openingStory1 = font.render('yang dikenal dengan desa vampir.', True,
                                    "Black")
        screen.blit(openingStory1, (530, 250))
        openingStory1 = font.render('Saat pagi hari, semuanya terlihat seperti desa pada umumnya.', True, "Black")
        screen.blit(openingStory1, (450, 270))
        openingStory1 = font.render('Namun saat malam tiba... ', True, "Black")
        screen.blit(openingStory1, (550, 300))
        openingStory1 = font.render('Sesosok vampir yang haus darah menghampiri setiap rumah', True, "Black")
        screen.blit(openingStory1, (450, 320))
        openingStory1 = font.render('yang ada di desa itu.', True, "Black")
        instruction = font.render('<< Press any key to continue >>', True, "Black")
        screen.blit(instruction, (600, 400))
        pygame.display.flip()
        clock.tick(60)

####### VAMPIRE IS TALKING ABOUT THE RULES
def dialogue_1():
    while True:
        screen.fill('#D74B4B')
        screen.blit(bgdialogue, (0, 0))
        screen.blit(dial_1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            # Press a key to go to the next scene.
            elif event.type ==pygame.KEYDOWN:
                return dialogue_2

        screen.blit(ballon_1, (0, 0))
        vampir_says = font.render('Penghuni di rumah itu pasti memiliki darah yang segar... RrRrr', True, "Black")
        screen.blit(vampir_says, (300, 400))
        instruction = font.render('<< Press any key to continue >>', True, "Black")
        screen.blit(instruction, (600, 450))
        pygame.display.flip()
        clock.tick(60)

def dialogue_2():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            # Press a key to go to the next scene.
            elif event.type ==pygame.KEYDOWN:
                return dialogue_3

        screen.blit(bgdialogue, (0, 0))
        screen.blit(ballon_2, (0, 0))
        screen.blit(dial_2, (0, 0))
        player_says = font.render('Hahaha apakah kamu tahu bahwa ini desa kekuasaanku?', True, "Black")
        screen.blit(player_says, (300, 400))
        instruction = font.render('<< Press any key to continue >>', True, "Black")
        screen.blit(instruction, (600, 450))
        pygame.display.flip()
        clock.tick(60)

def dialogue_3():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            # Press a key to go to the next scene.
            elif event.type ==pygame.KEYDOWN:
                return transition()

        screen.blit(bgdialogue, (0, 0))
        screen.blit(ballon_3, (0, 0))
        screen.blit(dial_3, (0, 0))
        player_says = font.render('Untuk bisa mengalahkanku, lempar saja aku dengan bawang putih.', True, "Black")
        screen.blit(player_says, (190, 350))
        player_says = font.render('Tapi tidak semudah itu... Hahaha...',True, "Black")
        screen.blit(player_says, (190, 370))
        player_says = font.render('Kamu hanya bisa melempar bawang putih, jika kamu berhasil menjawab pertanyaan dariku.',True, "Black")
        screen.blit(player_says, (190, 390))
        player_says = font.render('Dan jika kamu gagal menjawab pertanyaan dariku...', True, "Black")
        screen.blit(player_says, (190, 410))
        player_says = font.render('maka aku akan maju mendekati rumahmu dan kemudian ku hisap darahmu. Hahaha...', True, "Black")
        screen.blit(player_says, (190, 430))
        player_says = font.render('Apakah kamu siap menerima tantanganku?', True, "Black")
        screen.blit(player_says, (190, 450))
        instruction = font.render('<< Press any key to continue >>', True, "Black")
        screen.blit(instruction, (600, 500))
        pygame.display.flip()
        clock.tick(60)

####### THE TRANSITION
def transition():
    while True:
        pygame.mixer.music.fadeout(3000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start.top_rect.collidepoint(mouse_pos):
                    return game_loop()

        screen.fill('#D74B4B')
        screen.blit(nighttime, (0, 0))
        start_bar = pygame.image.load('png/startbar.png')
        screen.blit(start_bar, (0, 0))
        start0 = fontset.render('Are you ready?', True, "#FFFFFF")
        screen.blit(start0, (580, 350))
        start.draw()
        pygame.display.flip()
        clock.tick(60)

######## GAME LOOP
def game_loop():

    running = True

    ########################################

    ### Preliminary Setting for Score and Life
    Score = 0
    life = 3
    status = ""
    if Score == 10:
        status = "WON"
    if life == 0:
        status = "LOSE"

    ### Preliminary Setting for Help Buttons
    fiftyfifty=False
    callfriend=False
    golden=False
    converter = pyttsx3.init()

    ### Preliminary Setting for Questions and Answers
    questions = data.Q.to_list()
    # print(questions)
    corrects = data.C.to_list()
    # print(corrects)
    answers = data.filter(like="Alter")
    answers = answers.values.tolist()

    # shuffling answers options
    for i in range(len(answers)):
        random.shuffle(answers[i])

    inputAnswer = []
    notif = ""
    POPUPnotif = ""

    Q = questions
    A = answers
    C = corrects
    qa = list(zip(Q, A, C))
    # Shuffling Q&A
    random.shuffle(qa)
    Q, A, C = zip(*qa)
    print(qa[0])

    ### Creating the area for Q&A
    questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
    buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
    buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
    buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
    buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)

    ### Creating the area for Help Buttons
    fifty = help_button(1025,500,button_50,1)
    cF = help_button(1125,500,button_callafriend,1)
    gB = help_button(1225,500,button_golden,1)

    bt1_stat=True
    bt2_stat=True
    bt3_stat=True
    bt4_stat=True

    ### Preliminary Setting for Sounds and Musics
    salah = mixer.Sound('musicNsound/salah.mp3')
    benar = mixer.Sound('musicNsound/benar.mp3')
    mixer.music.load('musicNsound/backsoundsample.mp3')
    mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.4)

    kalah = mixer.Sound('musicNsound/womanscreams.wav')
    phonetut = mixer.Sound('musicNsound/tutut.mp3')

    ### Vampire Position base setting
    vamx = 950  # position vampire
    vamy = 150  # position vampire

    ### Garlic Bullet base setting
    # Ready: garlic appear on screen
    # Fire: garlic is moving
    garlic = pygame.image.load("png/garlic.png")
    garlicX = 300
    garlicY = 200
    garlicX_change = 20
    garlicY_change = 5
    garlic_state = "ready"

    dashboard_1 = pygame.image.load('png/dashboard.png')

    # Setting up the Sky for background
    cloudF_scroll = 0
    cloudF_speed = 8
    cloudB_scroll = 0
    cloudB_speed = 2

    #####################################################

    while running:

        clock.tick(fps)

        # Top Panel
        toppanel = pygame.image.load('png/malampolos.png')
        screen.blit(toppanel, (0, 0))
        # Bottom Panel
        bottompanel = pygame.image.load('png/bottomframe.png')
        screen.blit(bottompanel, (0, 400))
        screen.blit(dashboard_1, (0, 0))
        # Vampire Image
        screen.blit(vampireImage, (vamx, vamy))

        # Clouds and Moon Movement
        screen.blit(cloud_back, (cloudB_scroll, 0))
        screen.blit(cloud_back, (cloudB_scroll-800, 0))
        screen.blit(moon, (0, 0))
        screen.blit(cloud_front, (cloudF_scroll+1000, 0))
        cloudF_scroll -= cloudF_speed
        cloudB_scroll += cloudB_speed

        if abs(cloudF_scroll) > 1800:
            cloudF_scroll = 0
        if abs(cloudB_scroll) > 1350:
            cloudB_scroll = 0

        # Placing the Player's life icon in screen (ON)
        screen.blit(lifeIconON1, (1190, 430))
        screen.blit(lifeIconON1, (1140, 430))
        screen.blit(lifeIconON1, (1090, 430))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if fifty.rect.collidepoint(mouse_pos): ### Help button for 50:50
                    fifty.disable_button()
                    if fiftyfifty==False:
                        cek=0
                        i=0
                        lst_rand=[]
                        for i in range(4):
                            if(A[0][i]==C[0]):
                                cek = i
                            else:
                                lst_rand.append(i)
                        salah_1=random.randint(0,2)
                        salah_1=lst_rand[salah_1]
                        lst_rand.remove(salah_1)
                        salah_2=random.randint(0,1)
                        salah_2=lst_rand[salah_2]
                        print("jawaban benar ".format(A[0][i]))
                        print("Disable button {} dan {}".format(A[0][salah_1],A[0][salah_2]))

                        bantuan=True

                    fiftyfifty=True
                    notif=""

                if cF.rect.collidepoint(mouse_pos): ### Help button for Call a Friend
                    pygame.mixer.music.set_volume(0.0)
                    phonetut.play()
                    cF.disable_button()
                    if callfriend == False:
                        converter.setProperty('rate', 130)
                        converter.setProperty('volume', 0.9)
                        voices = converter.getProperty('voices')
                        voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
                        converter.setProperty('voice', voice_id)
                        answer_rand = random.randint(0, 3)
                        converter.say("                   Hello my Friend!")
                        converter.runAndWait()
                        answer_rand = [0, 1, 2, 3]
                        if bantuan == True:
                            for i in answer_rand:
                                if i == salah_1:
                                    answer_rand.remove(salah_1)
                                elif i == salah_2:
                                    answer_rand.remove(salah_2)
                            random_ = random.randint(0, 1)
                        else:
                            random_ = random.randint(0, 3)

                        notif = "My answer is " + A[0][answer_rand[random_]]
                        converter.say(notif)
                        converter.runAndWait()
                        pygame.mixer.music.set_volume(0.4)
                    callfriend = True

                if gB.rect.collidepoint(mouse_pos): ### Help button for Golden Button
                    if golden==False:
                        notif=notif = 'Jawabannya: {}'.format(C[0])
                    else:
                        notif=""
                    golden=True
                    gB.disable_button()

                if buttonOpt1.top_rect.collidepoint(mouse_pos): ### Button for Option Answer A
                    # buttonOpt1.check_click()
                    if bt1_stat==True:
                        inputAnswer = '{}'.format(A[0][0])
                        print(inputAnswer)
                        if inputAnswer == C[0]:
                            if garlic_state == "ready":
                                #garlicSound = mixer.Sound("")
                                #garlicSound.play()
                                garlicX = vamx - 10
                                garlicY = vamy - 20
                                garlic_shoot(garlicX,garlicY)
                            Score += 1
                            print('Good Job! Your score is ', str(Score))
                            notif = "OH NOOOOO!!!"
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa) #after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            benar.play()

                        else:
                            life -= 1
                            # Vampire's step/move
                            vamx -= 200
                            vamy -= 30
                            print('Incorrect! Your Score is ', str(Score))
                            print('Nyawa kamu: ', str(life))
                            notif = 'Haha Salah! Jawabannya: {}'.format(C[0])
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            salah.play()

                elif buttonOpt2.top_rect.collidepoint(mouse_pos): ### Button for Option Answer B
                    # buttonOpt2.check_click()
                    if bt2_stat==True:
                        inputAnswer = '{}'.format(A[0][1])
                        print(inputAnswer)
                        if inputAnswer == C[0]:
                            if garlic_state == "ready":
                                #garlicSound = mixer.Sound("")
                                #garlicSound.play()
                                garlicX = vamx - 10
                                garlicY = vamy - 20
                                garlic_shoot(garlicX,garlicY)
                            Score += 1
                            print('Good Job! Your score is ', str(Score))
                            notif = "TIDAKKKK! AWAS KAU!"
                            print(notif)
                            # Go to next questions
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            benar.play()
                        else:
                            life -= 1
                            # Vampire's step/move
                            vamx -= 200
                            vamy -= 30
                            print('Incorrect! Your Score is ', str(Score))
                            print('Nyawa kamu: ', str(life))
                            notif = 'Haha Salah! Jawabannya: {}'.format(C[0])
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            salah.play()

                elif buttonOpt3.top_rect.collidepoint(mouse_pos): ### Button for Option Answer C
                    # buttonOpt3.check_click()
                    if bt3_stat==True:
                        inputAnswer = '{}'.format(A[0][2])
                        print(inputAnswer)
                        if inputAnswer == C[0]:
                            if garlic_state == "ready":
                                #garlicSound = mixer.Sound("")
                                #garlicSound.play()
                                garlicX = vamx - 10
                                garlicY = vamy - 20
                                garlic_shoot(garlicX,garlicY)
                            Score += 1
                            print('Good Job! Your score is ', str(Score))
                            notif = "Rrrrrrr... AKAN KU BALAS KAU!"
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            benar.play()

                        else:
                            life -= 1
                            # Vampire' step/move
                            vamx -= 200
                            vamy -= 30
                            print('Incorrect! Your Score is ', str(Score))
                            print('Nyawa kamu: ', str(life))
                            notif = 'Haha Salah! Jawabannya: {}'.format(C[0])
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            salah.play()

                elif buttonOpt4.top_rect.collidepoint(mouse_pos): ### Button for Option Answer D
                    # buttonOpt4.check_click()
                    if bt4_stat==True:
                        inputAnswer = '{}'.format(A[0][3])
                        print(inputAnswer)
                        if inputAnswer == C[0]:
                            if garlic_state == "ready":
                                #garlicSound = mixer.Sound("")
                                #garlicSound.play()
                                garlicX = vamx - 10
                                garlicY = vamy - 20
                                garlic_shoot(garlicX,garlicY)
                            Score += 1
                            print('Good Job! Your score is ', str(Score))
                            notif = "TIDAAAAKKKK! Rrrrrrr..."
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            benar.play()
                        else:
                            life -= 1
                            # Vampire's Step/move
                            vamx -= 200
                            vamy -= 30
                            print('Incorrect! Your Score is ', str(Score))
                            print('Nyawa kamu: ', str(life))
                            notif = 'Haha Salah! Jawabannya: {}'.format(C[0])
                            print(notif)
                            # Go to the next question
                            qa = list(zip(Q, A, C))
                            print(qa[0])
                            del qa[0]
                            print(qa[0])
                            random.shuffle(qa)  # after we omit the first row (qa[0] we randomize the dataset again)
                            Q, A, C = zip(*qa)
                            questionText = fontset.render('{}'.format(Q[0]), True, '#FFFFFF')
                            buttonOpt1 = Button("A. {}".format(A[0][0]), 380, 40, (60, 510), 5)
                            buttonOpt2 = Button("B. {}".format(A[0][1]), 380, 40, (490, 510), 5)
                            buttonOpt3 = Button("C. {}".format(A[0][2]), 380, 40, (60, 565), 5)
                            buttonOpt4 = Button("D. {}".format(A[0][3]), 380, 40, (490, 565), 5)
                            bantuan=False
                            bt1_stat=True
                            bt2_stat=True
                            bt3_stat=True
                            bt4_stat=True
                            salah.play()

                ### FINAL SCORE AND LIFE (WIN/LOSE)
                # LOSE
                if (life == 0):
                    kalah.play()
                    pygame.mixer.music.fadeout(3000)
                    mixer.music.load('musicNsound/lose.mp3')
                    mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(0.4)
                    return closing_lose()
                #WIN
                if (Score == 10):
                    pygame.mixer.music.fadeout(3000)
                    mixer.music.load('musicNsound/wonsong.mp3')
                    mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(0.4)
                    return closing_win()

        # Player's Life / Life icon off if life -=1
        if life < 3:
            screen.blit(lifeIconOFF1, (1190, 430))
        if life < 2:
            screen.blit(lifeIconOFF1, (1140, 430))
        if life < 1:
            screen.blit(lifeIconOFF1, (1090, 430))
        if (inputAnswer == C[0]) or (inputAnswer != C[0]):
            POPUPnotif = fontset.render("{}".format(notif), True, "#FFFFFF")
            screen.blit(POPUPnotif, (850, 95))
        if Score == 0:
            screen.blit(vampirelife10, (1120, 30))
        if Score == 1:
            screen.blit(vampirelife9, (1120, 30))
        if Score == 2:
            screen.blit(vampirelife8, (1120, 30))
        if Score == 3:
            screen.blit(vampirelife7, (1120, 30))
        if Score == 4:
            screen.blit(vampirelife6, (1120, 30))
        if Score == 5:
            screen.blit(vampirelife5, (1120, 30))
        if Score == 6:
            screen.blit(vampirelife4, (1120, 30))
        if Score == 7:
            screen.blit(vampirelife3, (1120, 30))
        if Score == 8:
            screen.blit(vampirelife2, (1120, 30))
        if Score == 9:
            screen.blit(vampirelife1, (1120, 30))
        if Score == 10:
            screen.blit(vampirelife0, (1120, 30))

        # Drawing Questions and Answer buttons
        screen.blit(questionText, (100, 450))
        buttonOpt1.draw()
        buttonOpt2.draw()
        buttonOpt3.draw()
        buttonOpt4.draw()
        # Drwaing the Help buttons
        fifty.put(screen)
        gB.put(screen)
        cF.put(screen)

        ### CONDITION TO DISABLE THE HELP BUTTONS
        # 50:50
        if fiftyfifty:
            fifty.disable_button()
            screen.blit(button_50off, (1025,500))
            if bantuan:
                if(salah_1==0 or salah_2==0):
                    buttonOpt1.disable_button()
                    bt1_stat=False
                if(salah_1==1 or salah_2==1):
                    buttonOpt2.disable_button()
                    bt2_stat=False
                if(salah_1==2 or salah_2==2):
                    buttonOpt3.disable_button()
                    bt3_stat=False
                if(salah_1==3 or salah_2==3):
                    buttonOpt4.disable_button()
                    bt4_stat=False

        # GOLDEN BUTTON
        if golden:
            gB.disable_button()
            screen.blit(button_goldenoff, (1225,500))
        if callfriend:
            cF.disable_button()
            screen.blit(button_callafriendoff, (1125,500))

        # GARLIC MOVEMENT CONDITION
        if garlicY <=0:
            garlicY = 300
            garlic_state = "ready"

        if garlic_state == "fire":
            garlic_shoot(garlicX,garlicY)
            garlicX += garlicX_change
            garlicY += garlicY_change

        # Vampire Life board
        screen.blit(dashboard, (20, 0))
        print(status)
        pygame.display.update()

######## CLOSING SCENE
def closing_win():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.top_rect.collidepoint(mouse_pos):
                    pygame.quit()
                if tryagain.top_rect.collidepoint(mouse_pos):
                    return transition()

        screen.fill('#fbafca')
        screen.blit(closingbg, (0, 0))
        tryagain.draw()
        quit_button.draw()
        notif="HOREEEEE KAMU MENANG!"
        POPUPnotif = fontset.render("{}".format(notif), True, "#FFFFFF")
        screen.blit(POPUPnotif, (550, 250))
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(60)

def closing_lose():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Press a key to go to the next scene.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.top_rect.collidepoint(mouse_pos):
                    pygame.quit()
                if tryagain.top_rect.collidepoint(mouse_pos):
                    return transition()

        screen.fill('#fbafca')
        screen.blit(closingbg, (0, 0))
        tryagain.draw()
        quit_button.draw()
        notif = "YAHHH...KAMU KALAH!"
        POPUPnotif = fontset.render("{}".format(notif), True, "#FFFFFF")
        screen.blit(POPUPnotif, (577, 250))
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(60)

opening_story()
dialogue_1()
dialogue_2()
dialogue_3()
transition()
game_loop()
closing_win()
closing_lose()
pygame.quit()
