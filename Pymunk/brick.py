import random
import pygame 
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

pygame.font.init()


# font constant 
FONT = pygame.font.SysFont("comicsans" , 25)

# main screen variables
WIDTH , HEIGHT = 600 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60

# types of collision 
collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}

def draw(space , height , draw_options):
    WIN.fill((0 , 0 , 0))

    # rendering few texts 
    WIN.blit(FONT.render("MOVE WITH LEFT/RIGHT ARROWS , SPACE TO SPAWN A BALL" , 1 , (255 , 255 , 255)) , (5 , height - 40))

    WIN.blit(FONT.render("Press R to reset " , 1 , (255 , 255 , 255)) , (5 , height - 20))
    space.debug_draw(draw_options)

    pygame.display.update()

def spawn_ball(space , pos , direction):
    ball_body = pymunk.Body(1 , float("inf"))
    ball_body.position = pos

    ball_shape = pymunk.Circle(ball_body , 5)
    ball_shape.color = (0 , 255 , 0 , 100)
    ball_shape.elasticity = 1
    ball_shape.friction = 0.4
    ball_shape.collision_type = collision_types["ball"]
    ball_body.apply_impulse_at_local_point(Vec2d(*direction)) 

    # function for keepng the velocity of the ball constant 
    def constant_velocity(body , gravity , damping , dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity
    space.add(ball_body , ball_shape)

def setup_level(space , player_body ):

    # removing the balls and bricks
    for s in space.shapes[:] :
        if s.body.body_type == pymunk.Body.DYNAMIC and s.body not in [player_body]:
            space.remove(s.body, s)  

    spawn_ball(space , player_body.position + (0 , 40) , random.choice([(1 , 10) , (-1 , 10)]))    

    # spawning the bricks 
    for x in range(0 , 21):
        x = x * 22 + 75 

        for y in range(0 , 6):
            y = y * 15 + 400 
            brick_body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
            brick_body.position = x , y 

            shape = pymunk.Poly.create_box(brick_body, (20, 10))
            shape.elasticity = 0.8
            shape.friction = 0.5
            shape.color = pygame.Color("blue")
            shape.collision_type = collision_types["brick"]
            space.add(brick_body , shape)

    def remove_brick(arbiter , space , data ):
        shape = arbiter.shapes[0]
        space.remove(shape , shape.body)

    h = space.add_collision_handler(collision_types["brick"], collision_types["ball"] )
    h.separate = remove_brick

def main():

    run = True 
    clock = pygame.time.Clock()

    # physics stuff of pymunk module 
    space = pymunk.Space()
    space.gravity = ( 0 , 981)
    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    dt = 1/FPS

    static_lines = [
        pymunk.Segment(space.static_body, (50, 50), (50, 550), 2),
        pymunk.Segment(space.static_body, (50, 550), (550, 550), 2),
        pymunk.Segment(space.static_body, (550, 550), (550, 50), 2),
    ]

    for line in static_lines:
        line.color = pygame.Color("lightgray")
        line.elasticity = 1.0

    space.add(*static_lines)  

    # creating a sensor that removes anything which touches it 
    bottom = pymunk.Segment(space.static_body , (50 , 50) , (550, 50) ,2)
    bottom.sensor = True 
    bottom.collision_type = collision_types["bottom"]
    bottom.color = pygame.Color("red")

    def remove_first(arbiter , space , data):
        ball_shape = arbiter.shapes[0]
        space.remove(ball_shape , ball_shape.body)
        return True 

    h = space.add_collision_handler(collision_types["ball"], collision_types["bottom"])
    h.begin = remove_first
    space.add(bottom)

    # creating the player ship 
    player_body = pymunk.Body(500 , float("inf"))
    player_body.position = 300 , 100

    player_shape = pymunk.Segment(player_body , (-50 , 0) , (50 , 0)  , 8)
    player_shape.color = (255 , 0 , 0 , 100)
    player_shape.elasticity = 1
    player_shape.collision_type = collision_types["player"]

    def solve(arbiter , space , data):
        set_ = arbiter.contact_point_set
        if len(set_.points) > 0:
            player_shape = arbiter.shapes[0]
            width = (player_shape.b - player_shape.a).x
            delta = (player_shape.body.position - set_.points[0].point_a).x
            normal = Vec2d(0, 1).rotated(delta / width / 2)
            set_.normal = normal
            set_.points[0].distance = 0
        arbiter.contact_point_set = set_
        return True 

    h = space.add_collision_handler(collision_types["player"], collision_types["ball"])
    h.pre_solve = solve

    # restric movement of player to a straight line 
    move_joint = pymunk.GrooveJoint(space.static_body , player_body, (100 , 100) , (500 , 100), (0 ,0))
    space.add(player_body , player_shape , move_joint)


    # starting the game
    setup_level(space , player_body )

    while run :
        clock.tick(FPS)
        space.step(dt)
        draw(space , HEIGHT , draw_options)

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT :
                    player_body.velocity = (-600 , 0)
                elif event.key == pygame.K_RIGHT :
                    player_body.velocity = (600 , 0)

                elif event.key == pygame.K_SPACE :
                    spawn_ball(space , player_body.position + (0 , 40) , random.choice([(1 , 10) , (-1 , 10)]))

                elif event.key == pygame.K_r:
                    setup_level(space, player_body )

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_LEFT :
                    player_body.velocity = (0 , 0)

                if event.key == pygame.K_RIGHT :
                    player_body.velocity = (0 , 0)


if __name__ == '__main__':
    main()