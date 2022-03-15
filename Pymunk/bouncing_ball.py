import random
import pygame 
import pymunk 
import pymunk.pygame_util


# main screen constants
WIDTH , HEIGHT = 800 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Bouncing ball")
FPS = 60 

def draw(space , draw_options):
	WIN.fill((0 , 255 , 0))
	space.debug_draw(draw_options)
	pygame.display.update()

def create_boundaries(space , width , height) :
    rects = [
        [(width/2 , height - 15) , (width , 30)] , 
        [(width/2 , 15) , (width , 30)] ,
        [(15 , height/2) , (30 , height) ] , 
        [(width - 15 , height/2) , (30 , height)]
    ]

    for pos , size in rects :
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos 
        shape = pymunk.Poly.create_box(body , size)
        shape.elasticity = 1
        shape.friction = 0.5
        shape.color = (255 , 128 , 128 , 100)
        space.add(body , shape)

def create_static_visuals(space):
	static_body = space.static_body

	static_lines = [
		pymunk.Segment(static_body, (111.0, 600 - 280), (407.0, 600 - 246), 0.0),
		pymunk.Segment(static_body, (407.0, 600 - 246), (407.0, 600 - 343), 0.0),
	]

	for line in static_lines :
		line.color = (255 , 0 , 0 , 100)
		line.elasticity = 1
		line.friction = 0.8

		space.add(line)


def create_ball(space , radius , mass , pos) :
    body = pymunk.Body()
    body.position = pos 
    shape = pymunk.Circle(body , radius)
    shape.mass = mass 
    shape.color = (0 , 0 , 255 , 100)
    shape.elasticity = 1
    shape.friction = 0.4
    space.add(body , shape)
    return shape 


def main():
	run = True 
	clock = pygame.time.Clock()

	# main physics stuff
	space = pymunk.Space()
	space.gravity = (0 , 981)
	draw_options = pymunk.pygame_util.DrawOptions(WIN)

	create_boundaries(space , WIDTH , HEIGHT)
	create_static_visuals(space)

	# variables
	balls = []
	dt = 1/FPS

	while run :
		clock.tick(FPS)
		space.step(dt)
		draw(space , draw_options)

		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False 
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN :
				pressed_pos = pygame.mouse.get_pos()
				create_ball(space , 30 , 10 , pressed_pos)


if __name__ == '__main__':
	main()