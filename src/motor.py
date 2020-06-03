

class Motor:

    def __init__(self, pos, trans_speed):
        self.position = pos
        self.transport_speed = trans_speed
        self.is_base = True
        self.is_bound = False
