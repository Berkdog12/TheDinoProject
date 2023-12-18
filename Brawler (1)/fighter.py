import pygame

screen = pygame.display.set_mode((1000, 600))

class Fighter():
              def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
                self.player = player
                self.size = data[0]
                self.image_scale = data[1]
                self.offset = data[2]
                self.flip = flip
                self.animation_list = self.load_images(sprite_sheet, animation_steps)
                self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
                self.frame_index = 0
                self.image = self.animation_list[self.action][self.frame_index]
                self.update_time = pygame.time.get_ticks()
                self.rect = pygame.Rect((x, y, 80, 180))
                self.vel_y = 0
                self.running = False
                self.jump = False
                self.attacking = False
                self.attack_type = 0
                self.attack_cooldown = 0
                self.attack_sound = sound
                self.hit = False
                self.health = 100
                self.alive = True
                self.attackvar = 0
                self.iswarrioratck1 = False
                self.iswarrioratck2 = False
                self.iswizardatck1 = False
                self.iswizardatck2 = False


              def load_images(self, sprite_sheet, animation_steps):
                    #extract images from spritesheet
                    animation_list = []
                    for y, animation in enumerate(animation_steps):
                      temp_img_list = []
                      for x in range(animation):
                        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
                      animation_list.append(temp_img_list)
                    return animation_list


              def move(self, screen_width, screen_height, surface, target, round_over):
                    SPEED = 10
                    GRAVITY = 2
                    dx = 0
                    dy = 0
                    self.running = False
                    self.attack_type = 0

                    #get keypresses
                    key = pygame.key.get_pressed()

                    #can only perform other actions if not currently attacking
                    if self.attacking == False and self.alive == True and round_over == False:
                      #check player 1 controls
                      if self.player == 1:
                        #movement
                        if key[pygame.K_a]:
                          dx = -SPEED
                          self.running = True
                        if key[pygame.K_d]:
                          dx = SPEED
                          self.running = True
                        #jump
                        if key[pygame.K_w] and self.jump == False:
                          self.vel_y = -30
                          self.jump = True
                        #attack
                        if key[pygame.K_r] or key[pygame.K_t]:
                          #determine which attack type was used
                          if key[pygame.K_r]:
                            self.attackvar = 3
                            self.attack_type = 1
                            self.iswarrioratck1 = True
                          if key[pygame.K_t]:
                            self.attackvar = 4
                            self.attack_type = 2
                            self.iswarrioratck2 = True
                          self.attack(target)


                      #check player 2 controls
                      if self.player == 2:
                        #movement
                        if key[pygame.K_LEFT]:
                          dx = -SPEED
                          self.running = True
                        if key[pygame.K_RIGHT]:
                          dx = SPEED
                          self.running = True
                        #jump
                        if key[pygame.K_UP] and self.jump == False:
                          self.vel_y = -30
                          self.jump = True
                        #attack
                        if key[pygame.K_KP1] or key[pygame.K_KP2]:
                          #determine which attack type was used
                          if key[pygame.K_KP1]:
                            self.attackvar = 1
                            self.attack_type = 1
                            self.iswizardatck1 = True
                          if key[pygame.K_KP2]:
                            self.attackvar = 2
                            self.attack_type = 2
                            self.iswizardatck2 = True
                          self.attack(target)


                    #apply gravity
                    self.vel_y += GRAVITY
                    dy += self.vel_y

                    #ensure player stays on screen
                    if self.rect.left + dx < 0:
                      dx = -self.rect.left
                    if self.rect.right + dx > screen_width:
                      dx = screen_width - self.rect.right
                    if self.rect.bottom + dy > screen_height - 170:
                      self.vel_y = 0
                      self.jump = False
                      dy = screen_height - 170 - self.rect.bottom

                    #ensure players face each other
                    if target.rect.centerx > self.rect.centerx:
                      self.flip = False
                    else:
                      self.flip = True

                    #apply attack cooldown
                    if self.attack_cooldown > 0:
                      self.attack_cooldown -= 1

                    #update player position
                    self.rect.x += dx
                    self.rect.y += dy


                  #handle animation updates
              def update(self):
                    #check what action the player is performing
                    if self.health <= 0:
                      self.health = 0
                      self.alive = False
                      self.update_action(6)#6:death
                    elif self.hit == True:
                      self.update_action(5)#5:hit
                    elif self.attacking == True:
                      if self.attack_type == 1:
                        self.update_action(3)#3:attack1
                      elif self.attack_type == 2:
                        self.update_action(4)#4:attack2
                    elif self.jump == True:
                      self.update_action(2)#2:jump
                    elif self.running == True:
                      self.update_action(1)#1:run
                    else:
                      self.update_action(0)#0:idle

                    animation_cooldown = 50
                    #update image
                    self.image = self.animation_list[self.action][self.frame_index]
                    #check if enough time has passed since the last update
                    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                      self.frame_index += 1
                      self.update_time = pygame.time.get_ticks()
                    #check if the animation has finished
                    if self.frame_index >= len(self.animation_list[self.action]):
                      #if the player is dead then end the animation
                      if self.alive == False:
                        self.frame_index = len(self.animation_list[self.action]) - 1
                      else:
                        self.frame_index = 0
                        #check if an attack was executed
                        if self.action == 3 or self.action == 4:
                          self.attacking = False
                          self.attack_cooldown = 20
                        #check if damage was taken
                        if self.action == 5:
                          self.hit = False
                          #if the player was in the middle of an attack, then the attack is stopped
                          self.attacking = False
                          self.attack_cooldown = 20

              def hitbox(self, target):
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)

              def attack(self, target):
                    if self.attack_cooldown == 0:
                      #execute attack
                      self.attacking = True
                      self.attack_sound.play()
                      if self.iswarrioratck1  == True:
                        if self.flip == True:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) + 150, self.rect.y + 100, 1 * self.rect.width, 0.5 * self.rect.height)
                        else:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) - 75, self.rect.y + 100, 1 * self.rect.width, 0.5 * self.rect.height)
                      elif self.iswizardatck1 == True:
                        if self.flip == True:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) - 0, self.rect.y - 125 , 2 * self.rect.width, 3 * self.rect.height)
                        else:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y - 125 , 2 * self.rect.width, 3 * self.rect.height)
                      elif self.iswarrioratck2 == True:
                        if self.flip == True:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y + 100, 2.5 * self.rect.width, self.rect.height - 100)
                        else:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) - 50 , self.rect.y + 100, 2.5 * self.rect.width, self.rect.height - 100)
                      elif self.iswizardatck2 == True:
                        if self.flip == True:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) - 150, self.rect.y + 100, 3 * self.rect.width, self.rect.height - 100)
                        else:
                          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) + 50, self.rect.y + 100, 3 * self.rect.width, self.rect.height - 100)
                      #pygame.draw.rect(screen, (255,0,0), attacking_rect)
                      if attacking_rect.colliderect(target.rect):
                        if self.attackvar == 1:
                          target.health -= 15
                          self.attackvar == 0 
                        elif self.attackvar == 2:
                          target.health -= 10   
                          self.attackvar == 0
                        elif self.attackvar == 3:
                          target.health -= 30
                          self.attackvar == 0
                        elif self.attackvar == 4:
                          target.health -= 20
                          self.attackvar == 0
                        target.hit = True
                    self.attackvar == 0
                    self.iswarrioratck1 = False
                    self.iswarrioratck2 = False
                    self.iswizardatck1 = False
                    self.iswizardatck2 = False

              def update_action(self, new_action):
                    #check if the new action is different to the previous one
                    if new_action != self.action:
                      self.action = new_action
                      #update the animation settings
                      self.frame_index = 0
                      self.update_time = pygame.time.get_ticks()

              def draw(self, surface):
                    img = pygame.transform.flip(self.image, self.flip, False)
                    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))