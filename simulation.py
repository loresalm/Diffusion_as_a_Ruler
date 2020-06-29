# The aim of this script is to run the simulation using the components from src
# Imports:

from src.motor import Motor
from src.flagellum import Flagellum
from src.utility import *
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Configure here your simulation: (see table 1)
nb_mot = 200              # 0 motors
trans_speed = 2           # 1 µm/s
growth_mot = 0.00125      # 2 µm
dec = 0.01                # 3 µm/s
diff_coeff = 1.75         # 4 µm2/s
w_dist_pow = 2.85        # 5 Weibull dist. shape
w_dist_prefac = 10        # 6 Weibull dist. prefactor
avalanche_thresh = 30     # 7 motors
stop_t = 2400             # 8 s
init_length = 0           # 9 µm

param = [nb_mot, trans_speed, growth_mot,
         dec, diff_coeff, w_dist_pow,
         w_dist_prefac, avalanche_thresh, stop_t, init_length]

def reset_param():
    nb_mot = 200  # 0 motors
    trans_speed = 2  # 1 µm/s
    growth_mot = 0.00125  # 2 µm
    dec = 0.01  # 3 µm/s
    diff_coeff = 1.75  # 4 µm2/s
    w_dist_pow = 2.85  # 5 Weibull dist. shape
    w_dist_prefac = 10  # 6 Weibull dist. prefactor
    avalanche_thresh = 30  # 7 motors
    stop_t = 2400  # 8 s
    init_length = 0 # 9 µm

    return [nb_mot, trans_speed, growth_mot,
            dec, diff_coeff, w_dist_pow,
            w_dist_prefac, avalanche_thresh, stop_t, init_length]


def simulation(_param, track_motor = False):

    nb_motors = _param[0]               # motors
    transport_speed = _param[1]         # µm/s
    growth_per_motor = _param[2]        # µm
    decay = _param[3]                   # µm/s
    diffusion_coefficient = _param[4]   # µm2/s
    w_dist_power = _param[5]            # Weibull dist. shape
    w_dist_prefactor = _param[6]        # Weibull dist. prefactor
    avalanche_threshold = _param[7]     # motors
    stop_time = _param[8]               # s
    init_length = _param[9]             # µm

    # Initialization of the simulation:
    motors = [Motor(0, transport_speed) for m in range(nb_motors)]
    base_motors = len(motors)
    flagellum = Flagellum(init_length, decay, diffusion_coefficient)
    t = 0
    # Storage for results of the simulation:
    flag_length = []
    time = []
    count_flag_motor = []
    count_base_motors = []
    inj_per_sec = []
    pos_motor = []

    t_last_inj = 1
    # Main loop of the simulation:
    while t < stop_time:
        for m in motors:
            if not m.is_base:                               # m is out of the base -> m is on the flag.
                if m.is_bound:                              # m is bound to the flag.
                    m.position += m.transport_speed
                if m.position > flagellum.length:           # m is at the tip of the flag.
                    m.is_bound = False
                    flagellum.length += growth_per_motor
                    continue

                if not m.is_bound:                         # m is not bound to the flag.
                    if m.position <= 0:                     # m is at the base
                        m.is_base = True
                        base_motors += 1
                    else:                                   # m is not at the base
                        # TODO: check if this is the random walk they intended
                        direction = [1, -1]                       # TODO: step of diffudion??
                        m.position -= diffusion_coefficient * random.choice(direction)
                        if m.position > flagellum.length:
                            m.position -= 2*diffusion_coefficient
        if track_motor:
            pos_motor.append(motors[0].position)


        train_size = 0
        if base_motors > avalanche_threshold:  # lunch a train of motors
            t_x = (t-t_last_inj)
            t_last_inj = t
            # TODO: the 0.1 is hardcoded to make the simulation work check what I'm missing about the Weibull_dist
            # compute the size of the train
            x = (base_motors - avalanche_threshold)

            train_size =  x *  Weibull_dist(x/10, w_dist_prefactor, w_dist_power)
            # print(train_size, x)
            if train_size >= base_motors:
                train_size = base_motors

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

    return [flag_length, time, count_flag_motor, count_base_motors, inj_per_sec,pos_motor]

"""   # Simulations to test the parameter 
# A
pow_var = [[], []]
for i in range(0, 25):
    param[5] = i
    res = simulation(param)
    pow_var[0].append(i)
    pow_var[1].append(res[0][-1])

print("A complete")
param = reset_param()

# B
const_var = [[], []]
for i in range(1, 100):
    param[6] = i
    res = simulation(param)
    const_var[0].append(i)
    const_var[1].append(res[0][-1])

print("B complete")
param = reset_param()

# c
trash_var = [[], []]
for i in range(0, 200):
    param[7] = i
    res = simulation(param)
    trash_var[0].append(i)
    trash_var[1].append(res[0][-1])

print("C complete")
param = reset_param()

# D
act_trans_var = [[], []]
for i in range(0, 50):
    param[7] = i
    res = simulation(param)
    act_trans_var[0].append(i)
    act_trans_var[1].append(res[0][-1])

print("D complete")

# config of the plot
font_size = 10
params = {'axes.labelsize': font_size,
          'axes.titlesize': font_size,
          'xtick.labelsize': font_size,
          'ytick.labelsize': font_size
          }
plt.rcParams.update(params)
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(2, 2, figure=fig)


# do the plot
p1 = fig.add_subplot(gs[0, 0])
plt.title("A")
p1.plot(pow_var[0], pow_var[1], '.')
p1.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p1.set_xlabel('Weibull Power', fontsize=font_size)

p2 = fig.add_subplot(gs[0, 1])
plt.title("B")
p2.plot(const_var[0], const_var[1], '.')
p2.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p2.set_xlabel('Weibull Constant', fontsize=font_size)

p3 = fig.add_subplot(gs[1, 0])
plt.title("C")
p3.plot(trash_var[0], trash_var[1], '.')
p3.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p3.set_xlabel('Treshold', fontsize=font_size)

p4 = fig.add_subplot(gs[1, 1])
plt.title("D")
p4.plot(act_trans_var[0], act_trans_var[1], '.')
p4.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p4.set_xlabel('Active transport speed (µm/s)', fontsize=font_size)

plt.show()

"""

resB = simulation(param)

param = reset_param()
param[8] = 120

resA = simulation(param,True)

param = reset_param()

# config of the plot
font_size = 10
params = {'axes.labelsize': font_size,
          'axes.titlesize': font_size,
          'xtick.labelsize': font_size,
          'ytick.labelsize': font_size
          }
plt.rcParams.update(params)
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(1, 2, figure=fig)

p1 = fig.add_subplot(gs[0, 0])
plt.title("A")
p1.plot(resA[1], resA[5], label = "trace of one motor out of 200" )
p1.plot(resA[1], resA[0], label = "length of the flagellum " )
plt.ylim(0,8)
p1.set_ylabel('distance along flagellum (µm)', fontsize=font_size)
p1.set_xlabel('time (s)', fontsize=font_size)
p1.legend()
plt.grid()

p2 = fig.add_subplot(gs[0, 1])
plt.title("B")
p2.plot(resB[1], resB[0], '.')
p2.set_ylabel('Flagellar length (µm)', fontsize=font_size)
p2.set_xlabel('time (s)', fontsize=font_size)
plt.grid()


plt.show()




