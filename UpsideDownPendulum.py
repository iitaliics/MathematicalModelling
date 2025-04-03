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
    def __init__(self, surface_area, ball_mass, link_length, link_angle, link_angular_vel, link_angular_accel, cart_displacement, cart_velocity, cart_acceleration,):
        self.ball_mass = ball_mass
        self.surface_area = surface_area
        self.link_length = link_length 
        self.link_angle = link_angle    #up is 0, right is pi/2, down is pi/-pi
        self.link_angular_vel = link_angular_vel
        self.link_angular_accel = link_angular_accel
        self.cart_displacement = cart_displacement
        self.cart_velocity = cart_velocity
        self.cart_acceleration = cart_acceleration

#Ball motion
def calcAirResistanceTorque(thing):
    airDensity = 1
    area = thing.surface_area
    dragCoef = 0.4
    velocity = thing.link_length * thing.link_angular_vel
    try:
        torque = thing.link_length * 0.5 * airDensity * area * dragCoef * -math.copysign(math.pow(velocity, 2), velocity)
    except:
        print(torque)
    # print(force)
    return torque

def calcExternalForce(obj):
   
#    p_offset = 50
#    p_const = 0.4
#    d_const = -2
#    d_a_const = 3
    d_f = 0
    a_f = 0
    v_f = 0

    p_offset = 50
    p_const = 0.3
    d_const = -1
    d_a_const = 2

    v_f = d_const * obj.velocity
    a_f = d_a_const * obj.acceleration
    d_f = p_const * (goal_height - obj.height) + p_offset
#    if obj.height < goal_height:
#        d_f =
    sum_f = d_f + a_f + v_f
    f_total = sum_f * (obj.mass / 5)
   
    if f_total < 0: #or f_total > 0:
        return 0
    return f_total

def calcGravityTorque(obj):
    accel_g = -9.81
    total = accel_g * -math.sin(obj.link_angle)
    torque = total * obj.link_length
    return torque


def calcResultantTorque(thing, time):
    T_air = calcAirResistanceTorque(thing)
    T_grav = calcGravityTorque(thing)

    T_external = 0 # calcExternalForce(thing)
    T_result = T_air + T_grav + T_external
    return T_result


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

    

    for frame in range(len(data)):
        time = data[frame][0]

        cart_pos = data[frame][1]

        link_length = data[frame][2] * 100

        link_angle = data[frame][3]

        print(link_angle)

        screen.fill("black")
        pygame.draw.line(screen, (0, 0, 254), (50, height / 2), (width - 50, height / 2), 2) # track

        rect_width = 50
        rect_height = 10
        pygame.draw.rect(screen, (254, 0, 254), pygame.Rect((cart_pos - rect_width / 2), (height / 2 - rect_height / 2), rect_width, rect_height)) # cart


        pygame.draw.line(screen, (254, 0, 0), (cart_pos, height / 2), (cart_pos + link_length * math.sin(link_angle), height / 2 - link_length * math.cos(link_angle)), 2) # link

        pygame.draw.circle(screen, (0, 254, 0), (cart_pos + link_length * math.sin(link_angle), height / 2 - link_length * math.cos(link_angle)), radius=20, width=2) # ball

        pygame.display.update()

del_t = 0.005
#goal height
goal_height = 500

resolution = [1000, 500]

if __name__ == '__main__':
    #main loop

    plot = pygame.display.set_mode(((resolution[0] + 1), (resolution[1] + 1)))
    screen = pygame.display.set_mode(((resolution[0] + 1), (resolution[1] + 1)))

    obj = thing(1, 20, 1, 0.1, 0, 0, 750, 0, 0)
    time = 0

    data = []

    for _ in range(10500): # simulation
        obj.link_angular_accel = calcResultantTorque(obj, time)
        
        del_v = obj.link_angular_vel + obj.link_angular_accel * del_t 
        del_z = obj.link_angle + obj.link_angular_vel * del_t
               
        obj.link_angle = del_z + del_v * del_t
        obj.link_angular_vel = del_v

        if obj.link_angle < -math.pi:
            obj.link_angle = obj.link_angle + 2 * math.pi
        if obj.link_angle > math.pi:
            obj.link_angle = obj.link_angle - 2 * math.pi
           
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