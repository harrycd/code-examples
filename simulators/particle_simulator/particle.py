class Particle:
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0    # coordinates
        self.vx, self.vy, self.vz = 1, 1, 1     # velocities
        self.fx, self.fy, self.fz = 0, 0, 0     # forces
        self.mass = 1       # mass
        self.radius = 1     # radius of spherical particle
        self.colour = (0, 0, 0)     # colour of representation

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)
