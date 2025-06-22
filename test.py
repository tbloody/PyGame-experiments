# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 500
start_pos = pygame.Vector2(500, 100)
player_pos = start_pos.copy()


class Player():
    def __init__(self):
        self.pos = pygame.Vector2()
        self.radius = 40

    def get_box_collider(self):
        rect_x = self.pos.x - self.radius
        rect_y = self.pos.y - self.radius
        return pygame.Rect(rect_x, rect_y, self.radius*2, self.radius*2)

    def draw(self):
        pygame.draw.rect(screen, "blue", self.get_box_collider())
        pygame.draw.circle(screen, "purple", self.pos, self.radius)

    def get_closest_point_to(seklf, rect: pygame.Rect):
        closest_point = pygame.Vector2(player.pos.x, player.pos.y)
        if closest_point.x < rect.x:
            closest_point.x = rect.x
        if closest_point.x > rect.x + rect.width:
            closest_point.x = rect.x + rect.width
        if closest_point.y < rect.y:
            closest_point.y = rect.y
        if closest_point.y > rect.y + rect.height:
            closest_point.y = rect.y + rect.height
        return closest_point

    def collides_with_rect(self, rect: pygame.Rect):
        return player.collides_point(self.get_closest_point_to(rect))

    def collides_point(self, point: pygame.Vector2):
        x_dist = abs(self.pos.x - point.x)
        y_dist = abs(self.pos.y - point.y)
        return x_dist * x_dist + y_dist * y_dist < self.radius * self.radius

    def stick_to(self, rect: pygame.Rect):
        closest_point = self.get_closest_point_to(rect)
        closest_point_rect = pygame.Vector2()
        if closest_point.x < rect.x:
            closest_point_rect.x = rect.x
        elif closest_point.x > rect.x+rect.width:
            closest_point_rect.x = rect.x+rect.width
        else:
            closest_point_rect.x = closest_point.x

        if closest_point.y < rect.y:
            closest_point_rect.y = rect.y
        elif closest_point.y > rect.y+rect.height:
            closest_point_rect.y = rect.y+rect.height
        else:
            closest_point_rect.y = closest_point.y

        dist_x = closest_point.x - closest_point_rect.x
        dist_y = closest_point.y - closest_point_rect.y

        if dist_x >= 0:
            dist_x += 1
        else:
            dist_x -= 1

        if dist_y >= 0:
            dist_y += 1
        else:
            dist_y -= 1

        self.pos.x += dist_x
        self.pos.y += dist_y
        print("stick_to", closest_point, closest_point_rect)


class Wall():
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height

    def get_box_collider(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, "red", self.get_box_collider())


player = Player()
wall = Wall(pygame.Vector2(450, 450), 600, 100)
is_jumping = False
is_falling = False
jump_time = 0
fallspeed_modifier = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("cornflowerblue")

    # pygame.draw.circle(screen, "purple", player_pos, 40)
    player.draw()
    wall.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if not is_jumping:
            is_jumping = True
            jump_time = pygame.time.get_ticks()

    if keys[pygame.K_s]:
        player.pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player.pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player.pos.x += player_speed * dt
    if keys[pygame.K_ESCAPE]:
        running = False

    if is_jumping and jump_time > pygame.time.get_ticks()-100:
        player.pos.y -= player_speed * dt * 5
        fallspeed_modifier = 0.5

    elif is_jumping:
        is_falling = True
        if fallspeed_modifier < 5:
            fallspeed_modifier = fallspeed_modifier+0.1

    player.pos.y += player_speed * fallspeed_modifier * dt

    collides = player.collides_with_rect(wall.get_box_collider())

    if keys[pygame.K_r]:
        player.pos.x = start_pos.x
        player.pos.y = start_pos.y
        fallspeed_modifier = 2
        collides = False
    if not collides:
        player_pos.x = player.pos.x
        player_pos.y = player.pos.y
    else:
        is_jumping = False
        # TODO: getclosest point to new pos before collision
        # try ro fix by shifting up first
        player.pos.x = player_pos.x
        player.pos.y = player_pos.y
        player.stick_to(wall.get_box_collider())
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 120
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()
