import pygame, os, random, time

pygame.init()
gameWidth = 840
gameHeight = 640
picSize = 100
gameColumns = 5
gameRows = 4
padding = 10
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
bottomMargin = topMargin
selection1 = None
selection2 = None

#create the variables for the game
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Memory Game")
gameIcon = pygame.image.load('icon.png')

#set the icon
pygame.display.set_icon(gameIcon)

#load the background image
bgImage = pygame.image.load('background.png')
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bgImageRect = bgImage.get_rect()

#create a list of the cards
memoryPictures = []
for item in os.listdir('images/'):
    memoryPictures.append(item.split('.')[0])

#copy the list and extend it
memoryPicturesCopy = memoryPictures.copy()
memoryPictures.extend(memoryPicturesCopy)
memoryPicturesCopy.clear() #clear the copy list to save memory
random.shuffle(memoryPictures)

#load the images
memPics = []
memPicsRect = []
hiddenImages = []
for i in memoryPictures:
    picture = pygame.image.load(f'images/{i}.png')
    picture = pygame.transform.scale(picture, (picSize, picSize))
    memPics.append(picture)
    pictureRect = picture.get_rect()
    memPicsRect.append(pictureRect)

#set the positions of the cards
for i in range(len(memPicsRect)):
     memPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
     memPicsRect[i][1] = topMargin + ((picSize + padding) * (i % gameRows))
     hiddenImages.append(False)

#main loop
running = True
while running:
    screen.blit(bgImage, bgImageRect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in memPicsRect:
                if item.collidepoint(event.pos):
                    if selection1 != None:
                        selection2 = memPicsRect.index(item)
                        hiddenImages[selection2] = True
                    else:
                        selection1 = memPicsRect.index(item)
                        hiddenImages[selection1] = True
    #draw the cards
    for i in range(len(memPics)):
        if hiddenImages[i] == True:
            screen.blit(memPics[i], memPicsRect[i])
        else: #if the images are hidden, draw a white rectangle over them (the parameters are, screen, color, (x, y, width, height))
            pygame.draw.rect(screen, (255,255,255), (memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))

    pygame.display.update()
    #check if the cards match
    if selection1 != None and selection2 != None:
        if memoryPictures[selection1] == memoryPictures[selection2]:
             selection1, selection2 = None, None
        else:
            pygame.time.wait(1000)
            hiddenImages[selection1], hiddenImages[selection2] = False, False
            selection1, selection2 = None, None
    pygame.display.update()
    if all(hiddenImages):
        # create a font object
        font = pygame.font.Font(None, 64)
        # create a text surface
        text = font.render("You Win!", True, (0, 0, 0))
        # get the center position of the screen
        text_rect = text.get_rect(center=(gameWidth/2, gameHeight/2))
        # draw the text on the screen
        screen.blit(text, text_rect)
    pygame.display.update()
pygame.quit()
