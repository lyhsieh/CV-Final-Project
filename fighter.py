import pygame


class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, style_img_list, head_data):
        self.player = player
        self.size_x = data[0]
        self.size_y = data[1]
        self.image_scale = data[2]
        self.offset = data[3]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.defense = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.head_list = style_img_list
        self.head_count = 0
        self.head_size = head_data[0]
        self.head_scale = head_data[1]
        self.head_offset = head_data[2]
        self.head_img = pygame.image.load(self.head_list[self.head_count])   # start from the first style img (0)
        self.head_img = pygame.transform.scale(self.head_img, (self.head_size, self.head_size))


    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size_x, y * self.size_y, self.size_x, self.size_y)
                temp_img_list.append(pygame.transform.scale(
                    temp_img, (self.size_x * self.image_scale, self.size_y * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over, action):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # check player 1 controls
            if self.player == 1:
                # movement
                if key[pygame.K_a] or action[0]:    # raise left hand
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d] or action[1]:    # raise right hand
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_r] or key[pygame.K_t] or action[2] or action[3]:    # punch left or right
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_r] or action[2] or action[3]:
                        self.attack_type = 2
                    if key[pygame.K_t] or action[2] or action[3]:
                        self.attack_type = 1
                # defense
                if key[pygame.K_f] or action[4]:    # defense
                    self.defense = True

            # check player 2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT] or action[0]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT] or action[1]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_SPACE] or key[pygame.K_KP2] or action[2] or action[3]:
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_SPACE] or action[2] or action[3]:
                        self.attack_type = 2
                    if key[pygame.K_KP2] or action[2] or action[3]:
                        self.attack_type = 1
                # defense
                if key[pygame.K_m] or action[4]:    # defense
                    self.defense = True

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False   # when hit the ground
            dy = screen_height - 110 - self.rect.bottom

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates

    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:death
        elif self.hit == True:
            self.update_action(5)  # 5:hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3:attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:attack2
        elif self.jump == True:
            self.update_action(2)  # 2:jump
        elif self.running == True:
            self.update_action(1)  # 1:run
        elif self.defense == True:
            self.update_action(7)   # 7:defense
        else:
            self.update_action(0)  # 0:idle


        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 7:
                    self.defense = False


    def attack(self, target):
        if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (
                3 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                target.head_count += 1
                target.head_img = pygame.image.load(target.head_list[target.head_count])   # start from the first style img (0)
                target.head_img = pygame.transform.scale(target.head_img, (target.head_size, target.head_size))

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        head = pygame.transform.flip(self.head_img, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (
            self.offset[1] * self.image_scale)))
        surface.blit(head, (self.rect.x - (self.head_offset[0] * self.head_scale), self.rect.y - (
            self.head_offset[1] * self.head_scale)))
