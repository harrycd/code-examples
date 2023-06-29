from matplotlib import pyplot as plt, animation

from abc import ABC, abstractmethod
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import art3d


class Simulator(ABC):
    """ Core class handling common simulation functionalities"""
    simconf = None
    particles = []
    fig = None
    ax = None

    def run(self):
        """ Runs the simulator """

        self.check_setup()

        fig, ax = self.__generate_simulation_space()
        self.__add_bounding_box(ax)

        # Generate the initial graph
        graph = ax.scatter(
            xs=self.__get_particles_attribute('x'),
            ys=self.__get_particles_attribute('y'),
            zs=self.__get_particles_attribute('z'),
            color=self.__get_particles_attribute('colour'),
            s=[self.calc_size_3d(r) for r in self.__get_particles_attribute('radius')])

        plt.axis('off') # This way only the bounding box (literally) shows
        plt.gca().set_aspect("equal")   # Because markers are always symmetrical

        # Animate the particles
        anim = animation.FuncAnimation(
            fig,
            self.__update,
            fargs=[graph],
            interval=int(1000 / self.simconf.framerate),
            frames=self.simconf.total_frames)

        # Choose whether to display or export as video
        if not self.simconf.export_to_video:
            plt.show()
        else:
            writervideo = animation.FFMpegWriter(fps=60)
            anim.save('particle.mp4', writer=writervideo)
            plt.close()

    def check_setup(self):
        """ Checks if simulator parameters are initialised correctly """
        # Check if there are particles to run the simulation
        if len(self.particles) < 1:
            raise ValueError("The array of particles is empty or None.")
        if self.simconf is None:
            raise ImportError("Simulation configuration has not been loaded.")

    def __generate_simulation_space(self):
        """ Creates the figure and axes to display the simulation graphics"""
        fig = plt.figure(
            figsize=(self.simconf.fig_size, self.simconf.fig_size),
            dpi=self.simconf.dpi,
            layout='constrained'
        )
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlim(xmin=0, xmax=self.simconf.bbox_size)
        ax.set_ylim(ymin=0, ymax=self.simconf.bbox_size)
        ax.set_zlim(zmin=0, zmax=self.simconf.bbox_size)
        return fig, ax

    def __add_bounding_box(self, ax):
        """ Creates the graphics for the box that represents the simulation space boundaries"""
        bb = []
        # Add six rectangles
        for i in range(0, 6):
            bb.append(self.__get_rectangle(0, 0))
            ax.add_patch(bb[i])

        # Move the rectangles to construct the box
        art3d.pathpatch_2d_to_3d(bb[0], z=0, zdir="x")
        art3d.pathpatch_2d_to_3d(bb[1], z=0, zdir="y")
        art3d.pathpatch_2d_to_3d(bb[2], z=0, zdir="z")
        art3d.pathpatch_2d_to_3d(bb[3], z=self.simconf.bbox_size, zdir="x")
        art3d.pathpatch_2d_to_3d(bb[4], z=self.simconf.bbox_size, zdir="y")
        art3d.pathpatch_2d_to_3d(bb[5], z=self.simconf.bbox_size, zdir="z")

    def __get_rectangle(self, x, y):
        return Rectangle(xy=(x, y), width=self.simconf.bbox_size, height=self.simconf.bbox_size, linewidth=1,
                         color='gray',
                         alpha=0.3)

    def __get_particles_attribute(self, attribute):
        """ Creates an array containing the specified attribute values from the list of particles

        For example if attribute='x' and particles=[p1, p2] the function will return
        the list [p1.x, p2.x]
        :param attribute: the particle attribute to extract
        :type attribute: str
        :return: the list containing the specified attribute values
        :rtype: list
        """
        return [getattr(p, attribute) for p in self.particles]

    def __update(self, n: int, graph):
        """ Updates the simulation graphics """
        self.update_particles()
        graph._offsets3d = (
            self.__get_particles_attribute('x'),
            self.__get_particles_attribute('y'),
            self.__get_particles_attribute('z')
        )
        return graph

    def calc_size_3d(self, marker_radius):
        """Calculates the matplotlib size (marker, linewidth etc.) so that it matches the axes scale
        Important! If dpi increases and the graph exceeds the physical display limits then the marker
        size will be wrong.
        :param marker_radius: Radius of the marker based on plot units
        :type marker_radius: float

        """
        size = (82.5 * self.simconf.fig_size * marker_radius / self.simconf.bbox_size) ** 2
        return size

    @abstractmethod
    def update_particles(self):
        """ Updates properties of each particle"""
        pass
