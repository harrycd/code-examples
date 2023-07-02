import math
import numpy as np

from particle_simulator import simconf
from particle_simulator.simulator import Simulator
from particle_simulator.particle import Particle


class FreeParticlesSimulator(Simulator):
    def __init__(self):
        self.simconf = simconf  # Loads the simulator config
        particle_radius = 0.1   # Sets radius manually to override the default number of particles

        # The particles list is kept in two differently structured lists. One
        # for easy access to each particle and a second for processing by matplotlib
        self.particles_map, self.particles = get_part_particles(simconf.bbox_size, particle_radius)
        self.particles.insert(0, get_tool())  # adds the tool at index 0 for easy access

    def update_particles(self):
        """ Updates position for all particles including tool """

        # Reset locked flag
        for p in self.particles:
            p.locked = False

        update_tool_position(self.particles[0])
        update_part_position(self.particles[0], self.particles_map)


def update_tool_position(p: Particle):
    """ Updates tool's particle coordinates. The tool moves in a V shaped trajectory """
    if p.z <= 1.5:  # The tool reached max imprint depth
        p.vz = -p.vz
    if p.z > 4:  # The tool returned to base and process is finished
        p.vx = 0
        p.vz = 0
    p.z += p.vz * simconf.timestep
    p.x += p.vx * simconf.timestep


def update_part_position(tool: Particle, pmap):
    """ Updates the position of part particles """
    update_tool_collisions(tool, pmap)
    update_part_collisions(pmap)


def update_tool_collisions(tool, pmap):
    """ Updates part particles that collide with the tool """

    # Check collisions with tool (within the x, y, z of the tool)
    tri = int(tool.radius / pmap[0][0][0].radius)  # Tool's range of indexes (length/particle diameter)

    # find x index of pmap for tool position
    # tool.x-1 because the part starts from 1,1,1 and not from the beginning of axis (0,0,0)
    # 2 * radius because this is the initial distance between part particles
    tool_x_index = int((tool.x - 1) / (2 * pmap[0][0][0].radius))

    tool_y_index = int((tool.y - 1) / (2 * pmap[0][0][0].radius))

    tool_z_index = int((tool.z - 1) / (2 * pmap[0][0][0].radius))

    # Move colliding particles accordingly
    for x in range(tool_x_index - tri, tool_x_index + tri):
        if 0 <= x < len(pmap):  # Checks if index exists
            for y in range(tool_y_index - tri, tool_y_index + tri):
                if 0 <= y < len(pmap[0]):
                    for z in range(tool_z_index - tri, tool_z_index + tri):
                        if 0 <= z < len(pmap[0][0]):
                            set_post_collision_position(pmap[x][y][z], tool)
                            pmap[x][y][z].locked = True  # prevent push backs


def update_part_collisions(pmap):
    """ Updates part particles that collide with neighbouring particles """

    # Iterate over every particle, update post collision position and lock it
    x_max = len(pmap)
    y_max = len(pmap[0])
    z_max = len(pmap[0][0])
    for x in range(0, x_max):
        for y in range(0, y_max):
            for z in range(0, z_max):
                if not pmap[x][y][z].locked:
                    for pn in pmap[x][y][z].neighbours:
                        set_post_collision_position(pmap[x][y][z], pn)
                    pmap[x][y][z].locked = True


def set_post_collision_position(p_move, p_still):
    """ Calculates the position of a particle after a collision with another particle
    The 'other' particle is considered still

    :param p_move: The particle whose new coordinates are calculated
    :type p_move: Particle
    :param p_still: The particle that collided with the particle under observation
    :type p_still: Particle
    """
    dist = get_distance(p_still, p_move)

    # It is assumed that the particle will move along the line that connects
    # the centres of the two particles (since they are spherical). The particle
    # will move until the distance between two particles equals to the sum of
    # their radii. The length of movement is radius1 + radius2 - distance. The
    # rest of the formula is calculated using similar triangles. Therefore,
    # dx/distance = dx_move/move_length. At the end of movement the particles
    # touch each other but do not overlap.
    if dist < (p_still.radius + p_move.radius):
        p_move.x += (p_move.radius + p_still.radius - dist) * (p_move.x - p_still.x) / dist
        p_move.y += (p_move.radius + p_still.radius - dist) * (p_move.y - p_still.y) / dist
        p_move.z += (p_move.radius + p_still.radius - dist) * (p_move.z - p_still.z) / dist


def get_part_particles(bbox, particle_radius):
    """ Creates a 3D list representing the 3D structure of particles comprising the part """
    # Initially create a list which contains x lists. Each x list contains y lists with z elements
    # each. As a result, a particle can be referenced as particles[x][y][z]
    # where x, y, z are the corresponding indexes of the particle position in the part
    x_count = int((bbox - 2) / (2 * particle_radius))
    y_count = int((bbox - 2) / (2 * particle_radius))
    z_count = 5
    pmap = [[[Particle() for i in range(z_count)] for j in range(y_count)] for k in range(x_count)]

    # Initialise each particle
    for x in range(0, x_count):
        for y in range(0, y_count):
            for z in range(0, z_count):
                pmap[x][y][z].radius = particle_radius
                pmap[x][y][z].mass = pmap[x][y][z].radius ** 3  # For spheres with constant density

                pmap[x][y][z].x0 = 1 + x * 2 * pmap[x][y][z].radius
                pmap[x][y][z].y0 = 1 + y * 2 * pmap[x][y][z].radius
                pmap[x][y][z].z0 = 1 + z * 2 * pmap[x][y][z].radius
                pmap[x][y][z].x = pmap[x][y][z].x0
                pmap[x][y][z].y = pmap[x][y][z].y0
                pmap[x][y][z].z = pmap[x][y][z].z0

                pmap[x][y][z].vx, pmap[x][y][z].vy, pmap[x][y][z].vz = 0, 0, 0

                pmap[x][y][z].colour = 'darkslategray' if z % 2 == 0 else 'olive'

    # Add neighbours at initial position.
    # Neighbour particles are only the ones in contact (indexes: x+-1, y+-1, z+-1)
    for x in range(0, x_count):
        for y in range(0, y_count):
            for z in range(0, z_count):
                # Identify valid indexes of neighbours on each axis
                xns = [i for i in [x - 1, x + 1] if 0 <= i < x_count]
                yns = [i for i in [y - 1, y + 1] if 0 <= i < y_count]
                zns = [i for i in [z - 1, z + 1] if 0 <= i < z_count]

                # Store the neighbouring particles reference
                for xn in xns:
                    pmap[x][y][z].neighbours.append(pmap[xn][y][z])
                for yn in yns:
                    pmap[x][y][z].neighbours.append(pmap[x][yn][z])
                for zn in zns:
                    pmap[x][y][z].neighbours.append(pmap[x][y][zn])

    # Create a reference to the list that is flat (needed for matplotlib plotting
    # Flatten the list
    pflat = [x for z in pmap for y in z for x in y]
    return pmap, pflat


def get_tool():
    """ Initialises the particle that represents the tool """
    p = Particle()
    p.mass = 1
    p.radius = np.cbrt(p.mass)  # For spheres with constant density
    p.x0 = p.x = 1
    p.y0 = p.y = 4
    p.z0 = p.z = 4
    p.vx, p.vy, p.vz = 0.1, 0, -0.1
    p.colour = 'black'
    return p


def get_distance(p1: Particle, p2: Particle):
    """ Returns the distance between the centers of two particles """
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)


if __name__ == '__main__':
    sim = FreeParticlesSimulator()
    sim.run()
