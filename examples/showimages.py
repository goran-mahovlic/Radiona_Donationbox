import pygame, sys

pygame.init()
screen = pygame.display.set_mode((640,480))
images = []
images.append(pygame.image.load("/home/donationbox/Pictures/projectOneImage.png"))
images.append(pygame.image.load("/home/donationbox/Pictures/projectOneImage.png"))
show = 0
clock = pygame.time.Clock()
while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
         if event.key == pygame.K_SPACE:
            show = (show + 1) % len(images)
         
   screen.blit(images[show], (0 , 0))
   clock.tick(30)
   pygame.display.update()
