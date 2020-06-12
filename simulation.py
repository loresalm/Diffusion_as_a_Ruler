# The aim of this script is to run the simulation using the components from src
# Imports:

from src.motor import Motor
from src.flagellum import Flagellum
from src.utility import Weibull_dist
import random
import matplotlib.pyplot as plt


# Configure here your simulation: (see table 1)
nb_motors = 200                 # motors
transport_speed = 2             # µm/s
decay = 0.01                    # µm/s
diffusion_coefficient = 1.85    # µm2/s
avalanche_threshold = 30        # motors
growth_per_motor = 0.00125      # µm
stop_time = 2400                # s
w_dist_power = 2.85             # Weibull dist. shape
w_dist_prefactor = 10           # Weibull dist. prefactor


# Initialization of the simulation:
motors = [Motor(0, transport_speed) for m in range(nb_motors)]
base_motors = len(motors)
flagellum = Flagellum(0, decay, diffusion_coefficient)
t = 0


# Storage for results of the simulation:
flag_length = []
time = []
count_flag_motor = []
count_base_motors = []
inj_per_sec = []


# Main loop of the simulation:
while t < stop_time:
    for m in motors:
        if not m.is_base:                               # m is out of the base -> m is on the flag.
            if m.position > flagellum.length:           # m is at the tip of the flag.
                m.is_bound = False
                flagellum.length += growth_per_motor
                continue
            if m.is_bound:                              # m is bound to the flag.
                m.position += m.transport_speed
            else:                                       # m is not bound to the flag.
                if m.position <= 0:                     # m is at the base
                    m.is_base = True
                    base_motors += 1
                else:                                   # m is not at the base
                    # TODO: check if this is the random walk they intended
                    direction = [1, -1]                       # TODO: step of diffudion??
                    m.position -= diffusion_coefficient * random.choice(direction)
                    if m.position > flagellum.length:
                        m.position -= 2*diffusion_coefficient

    train_size = 0
    if base_motors > avalanche_threshold:  # lunch a train of motors

        # TODO: the 0.1 is hardcoded to make the simulation work check what I'm missing about the Weibull_dist
        # compute the size of the train
        x = 0.1*(base_motors - avalanche_threshold)
        train_size = base_motors*Weibull_dist(x, w_dist_prefactor, w_dist_power)

        # find the index of all trains that are in the base
        base_motor_index = [i for i, m in enumerate(motors) if m.is_base]

        # change the state of the trains that are in the base to False according to the size of the train
        if len(base_motor_index) > train_size:
            for i in range(int(train_size)):
                select_motor = base_motor_index[i]
                motors[select_motor].is_base = False
                motors[select_motor].is_bound = True
            base_motors -= train_size

        else:
            for select_motor in base_motor_index:
                motors[select_motor].is_base = False
                motors[select_motor].is_bound = True
            base_motors -= len(base_motor_index)

    if flagellum.length >= flagellum.decay_rate:
        flagellum.length -= flagellum.decay_rate
    t += 1

    # save the state of the simulation
    flag_length.append(flagellum.length)
    inj_per_sec.append(train_size)
    time.append(t)
    count_base_motors.append([m for m in motors if m.is_base])
    count_flag_motor.append([m for m in motors if not m.is_base])

plt.subplot(211)
plt.plot(time, flag_length,)
plt.ylabel("Flagellar length (µm)")
plt.xlabel("Time (s)")
plt.subplot(212)
plt.plot(flag_length, inj_per_sec,'.')
plt.ylabel("injection rate (motor/s)")
plt.xlabel("Flagellar length (µm)")

plt.show()





