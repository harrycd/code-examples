# Simulation configuration
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
timestep = float(config['simulator']['timestep'])
bbox_size = int(config['simulator']['bbox_size'])
fig_size = int(config['simulator']['fig_size'])
dpi = int(config['simulator']['dpi'])
particles_count = int(config['simulator']['particles_count'])
export_to_video = True if config['video']['export_to_video'] == 'yes' else False
framerate = int(config['video']['framerate'])
total_frames = int(config['video']['total_frames'])
