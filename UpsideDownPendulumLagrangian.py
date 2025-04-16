import random
import pygame
import math


"""
             ____
            /    \
           |  X   | ball
            \__\_/
                \                           Clockwise +ve
                 \
                  \ link
                   \
    track           \      
|_________________H==o==H_____________|
                    cart
"""

class thing:
    def __init__(self, surface_area, ball_mass, cart_mass, link_length, link_angle, link_angular_vel, link_angular_accel, cart_displacement, cart_velocity, cart_acceleration,):
        self.ball_mass = ball_mass
        self.cart_mass = cart_mass
        self.surface_area = surface_area
        self.link_length = link_length 
        self.link_angle = link_angle    #up is 0, right is pi/2, down is pi/-pi
        self.link_angular_vel = link_angular_vel
        self.link_angular_accel = link_angular_accel
        self.cart_displacement = cart_displacement
        self.cart_velocity = cart_velocity
        self.cart_acceleration = cart_acceleration

def calculate_link_tension(thing):
    accel_g = 9.81
    link_T = (obj.ball_mass * math.pow(obj.link_angular_vel, 2)) - (obj.ball_mass * accel_g * math.cos(obj.link_angle))
    return link_T

def calculate_cart_friction(thing):
    return 0.05 * thing.cart_velocity
    coefficient = 0.05 if thing.cart_velocity > 0 else 0.1
    return coefficient * (thing.cart_mass + calculate_link_tension(thing) * math.cos(thing.link_angle))

def applied_cart_force(thing):
    #want to control the system based on the pendulum variables and the cart position

    #Goal positions
    cart_goal_position = 5
    pendulum_goal_angle = 0

    #offsets
    # cart_goal_position = 5
    # pendulum_goal_angle = 0

    #gains
    p_cart = -10
    p_angle = 700
    d_ang_vel = -100
    dd_ang_accel = 0

    horizon_modifier = 1 if math.cos(thing.link_angle) > 0 else -1

    

    cart_f = p_cart * (cart_goal_position - thing.cart_displacement)
    angle_f = p_angle * ((pendulum_goal_angle - thing.link_angle))
    ang_vel_f = d_ang_vel * (thing.link_angular_vel)
    ang_accel_f = dd_ang_accel * (thing.link_angular_accel) * horizon_modifier


    sum_f = cart_f + angle_f + ang_vel_f + ang_accel_f

    return sum_f

def calculate_air_resistance(thing):
    airDensity = 1
    area = thing.surface_area
    dragCoef = 0.4
    velocity = thing.link_length * thing.link_angular_vel #- thing.cart_velocity * math.cos(thing.link_angle)
    try:
        torque = thing.link_length * 0.5 * airDensity * area * dragCoef * (velocity * velocity) * math.copysign(1, velocity)
        return torque
    except:
        print(velocity)
    

def calculate_trolley_acceleration(thing):
    mp = thing.ball_mass
    mt = thing.cart_mass
    l = thing.link_length
    thetadd = thing.link_angular_accel
    thetad = thing.link_angular_vel
    theta = thing.link_angle

    F_ext = applied_cart_force(thing)
    F_friction = calculate_cart_friction(thing)

    cart_accel = -((mp * l * (thetadd * math.cos(theta) - math.pow(thetad, 2) * math.sin(theta))) / (mt + mp)) - F_friction + F_ext / mt

    return cart_accel

def calculate_pendulum_angular_acceleration(thing):
    mp = thing.ball_mass
    mt = thing.cart_mass
    l = thing.link_length
    xdotdot = thing.cart_acceleration
    theta = thing.link_angle

    T_air_resistance = calculate_air_resistance(thing)

    pendulum_ang_accel = ((l * xdotdot * math.cos(theta) - l * (-9.81) * math.sin(theta)) / math.pow(l, 2)) - T_air_resistance

    return pendulum_ang_accel


#Cart motion (controllable)

def graph(data):
    graph_division_size = resolution[1] / 3
    
    chart_max = max(val for _, val, _, _ in data)
    chart_min = min(val for _, val, _, _ in data)

    chart_height = chart_max - chart_min
    chart_length = len(data)

    # Corrected scaling factor calculation
    scaled_height = graph_division_size / chart_height


    vel_max = max(val for _, _, val, _ in data)
    vel_min = min(val for _, _, val, _ in data)
    
    vel_height = vel_max - vel_min

    scaled_vel = graph_division_size / vel_height


    acc_max = max(val for _, _, _, val in data)
    acc_min = min(val for _, _, _, val in data)
    
    acc_height = acc_max - acc_min

    scaled_acc = graph_division_size / acc_height

    for index in range(chart_length - 1):

        # Vel
        x_1 = (index / chart_length) * resolution[0]
        y_1 = 2 * graph_division_size - (data[index][2] - vel_min) * scaled_vel

        x_2 = ((index + 1) / chart_length) * resolution[0]
        y_2 = 2 * graph_division_size - (data[index + 1][2] - vel_min) * scaled_vel
        # Draw vel
        pygame.draw.line(plot, (255, 10, 10), (x_1, y_1), (x_2, y_2), 2)

        # Accel
        x_1 = (index / chart_length) * resolution[0]
        y_1 = 3 * graph_division_size - (data[index][3] - acc_min) * scaled_acc

        x_2 = ((index + 1) / chart_length) * resolution[0]
        y_2 = 3 * graph_division_size - (data[index + 1][3] - acc_min) * scaled_acc
        # Draw acc
        pygame.draw.line(plot, (10, 10, 255), (x_1, y_1), (x_2, y_2), 2)


        # HEIGHT
        x_1 = (index / chart_length) * resolution[0]
        y_1 = graph_division_size - (data[index][1] - chart_min) * scaled_height

        x_2 = ((index + 1) / chart_length) * resolution[0]
        y_2 = graph_division_size - (data[index + 1][1] - chart_min) * scaled_height

        # Debugging output to check values
        # print(f"Index: {index}, x_1: {x_1}, y_1: {y_1}, x_2: {x_2}, y_2: {y_2}")

        # Draw height
        pygame.draw.line(plot, (255, 255, 255), (x_1, y_1), (x_2, y_2), 2)

        



        # GRID
        if index % (0.1 * chart_length) == 0:
            pygame.draw.line(plot, (100, 100, 100), ((index / chart_length) * resolution[0], 0), ((index / chart_length) * resolution[0], resolution[1]), 2)
    
    # goal_height
    pygame.draw.line(plot, (0, 255, 0), (0, graph_division_size - (goal_height - chart_min) * scaled_height), (resolution[0], graph_division_size - (goal_height - chart_min) * scaled_height), 2)

    # zero height
    pygame.draw.line(plot, (150, 150, 150), (0, graph_division_size - (-chart_min * scaled_height)), (resolution[0], graph_division_size - (-chart_min * scaled_height)), 2)

    # zero vel
    pygame.draw.line(plot, (100, 0, 0), (0, 2 * graph_division_size - (-vel_min * scaled_vel)), (resolution[0], 2 * graph_division_size - (-vel_min * scaled_vel)), 2)

    # zero acc
    pygame.draw.line(plot, (0, 0, 100), (0, 3 * graph_division_size - (-acc_min * scaled_acc)), (resolution[0], 3 * graph_division_size - (-acc_min * scaled_acc)), 2)


def playback(data):
    width = 1000
    height = 500

    clock = pygame.time.Clock()


    for frame in range(len(data)):
        time = data[frame][0]

        cart_pos = data[frame][1] * 95 + 2.5

        link_length = data[frame][2] * 200

        link_angle = data[frame][3]

        screen.fill("black")
        pygame.draw.line(screen, (0, 0, 254), (50, height / 2), (width - 50, height / 2), 2) # track

        rect_width = 50
        rect_height = 10
        pygame.draw.rect(screen, (254, 0, 254), pygame.Rect((cart_pos - rect_width / 2), (height / 2 - rect_height / 2), rect_width, rect_height)) # cart


        pygame.draw.line(screen, (254, 0, 0), (cart_pos, height / 2), (cart_pos + link_length * -math.sin(link_angle), height / 2 - link_length * math.cos(link_angle)), 2) # link

        pygame.draw.circle(screen, (0, 254, 0), (cart_pos + link_length * -math.sin(link_angle), height / 2 - link_length * math.cos(link_angle)), radius=20, width=2) # ball
        clock.tick(60)
        pygame.display.update()

del_t = 0.01
#goal height
goal_height = 500

resolution = [1000, 500]

if __name__ == '__main__':
    #main loop

    plot = pygame.display.set_mode(((resolution[0] + 1), (resolution[1] + 1)))
    screen = pygame.display.set_mode(((resolution[0] + 1), (resolution[1] + 1)))

    obj = thing(
        surface_area=1,
        ball_mass=50,
        cart_mass=20,
        link_length=1, 
        link_angle=0.1, 
        link_angular_vel=0, 
        link_angular_accel=0,
        cart_displacement=5, 
        cart_velocity=0, 
        cart_acceleration=0)
    time = 0

    data = []

    for _ in range(5000): # simulation
        obj.link_angular_accel = calculate_pendulum_angular_acceleration(obj)
        obj.cart_acceleration = calculate_trolley_acceleration(obj)
        
        obj.link_angular_vel = obj.link_angular_vel + obj.link_angular_accel * del_t
        obj.link_angle = obj.link_angle + obj.link_angular_vel * del_t

        obj.cart_velocity = obj.cart_velocity + obj.cart_acceleration * del_t
        obj.cart_displacement = obj.cart_displacement + obj.cart_velocity * del_t

        if obj.cart_displacement > 10:
            # obj.link_angular_vel += obj.cart_velocity * math.cos(obj.link_angle)
            obj.cart_displacement = 10
            obj.cart_acceleration = 0
            obj.cart_velocity = 0

            

        if obj.cart_displacement < 0:
            # obj.link_angular_vel += obj.cart_velocity * math.cos(obj.link_angle)
            obj.cart_displacement = 0
            obj.cart_acceleration = 0
            obj.cart_velocity = 0
           
            # obj.velocity = 0
            # obj.acceleration = calcResultantAccel(obj, time)
        
        time += del_t
        data.append([time, obj.cart_displacement, obj.link_length, obj.link_angle])
        # print("time: ", int(time), "        height: ", obj.height,  "       vel: ", obj.velocity,  "        accel: ", obj.acceleration)
    plot.fill("black")
    # graph(data)
    pygame.display.update()
    

    done = False
    while not done:

        
        

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close

                done = True
        
        playback(data)