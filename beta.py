import sys
import os
import pygame
from pygame.locals import *
from pygame.color import *
from pymunk.pygame_util import draw_space, from_pygame, to_pygame
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame
class Pig:
     def __init__(self):
        mass = .5
        ball_radius = 25
        #~ moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        self.body =  pymunk.Body(mass, 10)
        self.shape =pymunk.Circle(self.body, 20)
        self.shape.color=pygame.Color(255, 255, 0)
        mp=from_pygame( (pygame.mouse.get_pos()), screen )
        self.body.position=(mp[0],mp[1])
         
        self.shape.ignore_draw =True
       
def create_pig():
    ping=Pig()
    return ping.body, ping.shape
class Ball():
    def __init__(self):
        mass = 5
        ball_radius = 25
        #~ moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        self.body =  pymunk.Body(mass, 10)
        self.shape =pymunk.Circle(self.body, 20)
        self.shape.friction = 1
        #~ self.shape.draw_shape()
        #~ self.shape.sensor= True
        self.shape.collision_type = 1
        self.shape.color=pygame.Color(255, 255, 0,100)
        
        self.shape.ignore_draw = True
        #~ return ball_body, ball_shape
def create_ball():
    ball=Ball()
    return ball.body, ball.shape


width, height = 900,600
space = pymunk.Space()
screen = pygame.display.set_mode((width,height))
def main():
    
     
    ### PyGame init
    pygame.init()
    
    clock = pygame.time.Clock()
    running = True


    ### Physics stuff
    
    space.gravity = 0,-980
    static= [pymunk.Segment(space.static_body, (10, 50), (10, 590), 5),
        pymunk.Segment(space.static_body, (500, 200), (900,200), 5),
        pymunk.Segment(space.static_body, (500, 100), (900,100), 5),
         pymunk.Segment(space.static_body, (500, 300), (900,300), 5),
         pymunk.Segment(space.static_body, (500, 100), (450,150), 5),
         pymunk.Segment(space.static_body, (10, 590), (890, 590), 5)
                ]

    for s in static:
        s.friction = 1.
        s.group = 1
    space.add(static)
    # "Cannon" that can fire arrows
    cannon_body = pymunk.Body(10, 10)
    cannon_shape = pymunk.Circle(cannon_body, .1)
    cannon_shape.ignore_draw=True
    #~ cannon_shape.sensor = True
    cannon_body.position = 100,150
    #~ space.add(cannon_shape)

    ball_body,ball_shape = create_ball()
    pig_body,pig_shape = create_pig()
    #~ ball_shape.ignore_draw=True
    


    while running:
        start=Vec2d (100,300)
        for event in pygame.event.get():
            mp=from_pygame( (pygame.mouse.get_pos()), screen )
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                running = False
            elif  pygame.mouse.get_pressed()[1]:
                pig_body.position=mp
                space.add(pig_body)
                space.add(pig_shape)
                pig_body, pig_shape = create_pig()
                print len(space.shapes)
                break
            elif event.type == pygame.MOUSEMOTION and  pygame.mouse.get_pressed()[0]:
                cannon_body.position =Vec2d (mp[0],mp[1])
                print cannon_body.position
            elif event.type == pygame.MOUSEBUTTONUP and  pygame.mouse.get_pressed()[1]==False:
                diff =  -1*(Vec2d(mp)  - start)
                print("abs="+str(diff))
                cannon_body.position =start
                
                impulse = diff* 75
                ball_body.apply_impulse(impulse.rotated(ball_body.angle))

                space.add(ball_body)
                
                #~ ball_shape.ignore_draw=True
                ball_body, ball_shape = create_ball()
                space.add(ball_shape)
                
                
        mouse_position = from_pygame( Vec2d(pygame.mouse.get_pos()), screen )
        cannon_body.angle = (mouse_position - cannon_body.position).angle
        # move the unfired ball together with the cannon
        ball_body.position = cannon_body.position 
        ball_body.angle = cannon_body.angle


        ### Clear screen
        screen.fill(pygame.color.THECOLORS["white"])

        ### Draw stuff
        background = os.path.join("bgsl.png")
        background_surface = pygame.image.load(background)
        screen.blit(background_surface, (0,0)) 
        
        #~ animation_offset = 32*0
        col=[]
        pigs=[]
        for x in space.shapes:
            if x.body.mass>1:
                col.append(x)
            else:
                pigs.append(x)
        #~ print len(col)
        for x in col:
            tem=x.body.position
            tem=list(tem)
            pos=tem[0]-20,tem[1]+20
            #~ position=5
            #~ print (s)
            screen.blit(img, to_pygame(pos, screen))
        for x in pigs:
            tem=x.body.position
            tem=list(tem)
            pos=tem[0]-30,tem[1]+20
            #~ position=5
            #~ print (s)
            screen.blit(pigimg, to_pygame(pos, screen))
        draw_space(screen, space)


        pygame.display.flip()

        ### Update physics
        fps = 60
        dt = 1./fps
        space.step(dt)
        

        clock.tick(fps)
img = pygame.image.load("abs.png")
pigimg = pygame.image.load("logos.png")
if __name__ == '__main__':
    sys.exit(main())

