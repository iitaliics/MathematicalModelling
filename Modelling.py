import random
import pygame
import math


class thing:
    def __init__(self, surfaceArea, mass, height, velocity, acceleration):
        self.surfaceArea = surfaceArea
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.acceleration = acceleration

def calcAirResistanceForce(thing):
    airDensity = 1
    area = thing.surfaceArea
    dragCoef = 0.4
    velocity = thing.velocity

    try:
        force = 0.5 * airDensity * area * dragCoef * -math.copysign(math.pow(velocity, 2), velocity)
    except:
        print(velocity)
    # print(force)
    return force

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



def calcResultantAccel(thing, time):
    F_air = calcAirResistanceForce(thing)
    F_grav = -9.81 * thing.mass

    F_external = calcExternalForce(thing)
    F_result = F_air + F_grav + F_external
    return F_result / thing.mass

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
        pygame.draw.line(screen, (255, 10, 10), (x_1, y_1), (x_2, y_2), 2)

        # Accel
        x_1 = (index / chart_length) * resolution[0]
        y_1 = 3 * graph_division_size - (data[index][3] - acc_min) * scaled_acc

        x_2 = ((index + 1) / chart_length) * resolution[0]
        y_2 = 3 * graph_division_size - (data[index + 1][3] - acc_min) * scaled_acc
        # Draw acc
        pygame.draw.line(screen, (10, 10, 255), (x_1, y_1), (x_2, y_2), 2)


        # HEIGHT
        x_1 = (index / chart_length) * resolution[0]
        y_1 = graph_division_size - (data[index][1] - chart_min) * scaled_height

        x_2 = ((index + 1) / chart_length) * resolution[0]
        y_2 = graph_division_size - (data[index + 1][1] - chart_min) * scaled_height

        # Debugging output to check values
        # print(f"Index: {index}, x_1: {x_1}, y_1: {y_1}, x_2: {x_2}, y_2: {y_2}")

        # Draw height
        pygame.draw.line(screen, (255, 255, 255), (x_1, y_1), (x_2, y_2), 2)

        



        # GRID
        if index % (0.1 * chart_length) == 0:
            pygame.draw.line(screen, (100, 100, 100), ((index / chart_length) * resolution[0], 0), ((index / chart_length) * resolution[0], resolution[1]), 2)
    
    # goal_height
    pygame.draw.line(screen, (0, 255, 0), (0, graph_division_size - (goal_height - chart_min) * scaled_height), (resolution[0], graph_division_size - (goal_height - chart_min) * scaled_height), 2)

    # zero height
    pygame.draw.line(screen, (150, 150, 150), (0, graph_division_size - (-chart_min * scaled_height)), (resolution[0], graph_division_size - (-chart_min * scaled_height)), 2)

    # zero vel
    pygame.draw.line(screen, (100, 0, 0), (0, 2 * graph_division_size - (-vel_min * scaled_vel)), (resolution[0], 2 * graph_division_size - (-vel_min * scaled_vel)), 2)

    # zero acc
    pygame.draw.line(screen, (0, 0, 100), (0, 3 * graph_division_size - (-acc_min * scaled_acc)), (resolution[0], 3 * graph_division_size - (-acc_min * scaled_acc)), 2)


F_grav = -9.81
del_t = 0.01
#goal height
goal_height = 500

resolution = [2000, 1200]

if __name__ == '__main__':
    #main loop

    screen = pygame.display.set_mode(((resolution[0] + 1), (resolution[1] + 1)))

    obj = thing(1, 500, 1000, 0, 0)
    time = 0

    data = []

    for _ in range(10000):
        obj.acceleration = calcResultantAccel(obj, time)
        del_v = obj.velocity + obj.acceleration * del_t 
        del_z = obj.height + obj.velocity * del_t
               
        obj.height = del_z + del_v * del_t
        obj.velocity = del_v

        if obj.height < -50:
            obj.height = -50
            obj.velocity = 0
            obj.acceleration = calcResultantAccel(obj, time)
        
        time += del_t
        data.append([time, obj.height, obj.velocity, obj.acceleration])
        print("time: ", int(time), "        height: ", obj.height,  "       vel: ", obj.velocity,  "        accel: ", obj.acceleration)
    screen.fill("black")
    graph(data)
    
    pygame.display.update()
    

    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True