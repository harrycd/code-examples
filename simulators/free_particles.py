import math

import numpy as np
from random import random

from particle_simulator import simconf
from particle_simulator.simulator import Simulator
from particle_simulator.particle import Particle


class FreeParticlesSimulator(Simulator):
    def __init__(self):
        self.particles = [get_particle(i) for i in range(0, simconf.particles_count)]
        self.simconf = simconf

    def update_particles(self):
        for i in range(0, len(self.particles)):
            update_particle_position(self.particles[i])
            update_wall_collisions(self.particles[i])

        # update_particle_collisions(self.particles)


def update_particle_position(p: Particle):
    p.x += p.vx * simconf.timestep
    p.y += p.vy * simconf.timestep
    p.z += p.vz * simconf.timestep


def update_wall_collisions(p: Particle):
    """Detects the collision of a particle with the bounding box and returns the particle's updated velocity"""
    if not p.radius <= p.x <= (simconf.bbox_size - p.radius):
        p.vx = -p.vx
    if not p.radius <= p.y <= (simconf.bbox_size - p.radius):
        p.vy = -p.vy
    if not p.radius <= p.z <= (simconf.bbox_size - p.radius):
        p.vz = -p.vz


def update_particle_collisions(particles: list[Particle]):
    particles.sort(key=lambda x: x.x)
    # iterate over elements if two elements are closer than radius + radius then adjust velocity.
    for i in range(1, len(particles)):
        if check_collision(particles[i], particles[i - 1]):
            pass


def check_collision(p1: Particle, p2: Particle):
    min_distance = p1.radius + p2.radius
    if (
            abs(p1.x - p2.x) < min_distance and
            abs(p1.y - p2.y) < min_distance and
            abs(p1.y - p2.y) < min_distance
    ):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        dz = p1.y - p2.y

        if math.sqrt(dx * dx + dy * dy + dz * dz) < min_distance:
            return True

    return False


def get_particle(index=0):
    p = Particle()
    p.x = 1 + (index % (simconf.bbox_size - 2))
    p.y = int(1 + ((index / (simconf.bbox_size - 2)) % (simconf.bbox_size - 2)))
    p.z = int(index / ((simconf.bbox_size - 2) * (simconf.bbox_size - 2))) + 1
    p.vx, p.vy, p.vz = random(), random(), random()
    p.mass = 0.01 + 0.1 * random()
    p.radius = np.cbrt(p.mass)  # For spheres with constant density
    p.colour = (0.5 - random() / 2, 0.5 - random() / 2, 0.5 - random() / 2)
    return p


if __name__ == '__main__':
    sim = FreeParticlesSimulator()
    sim.run()
