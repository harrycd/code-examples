# Simulation configuration
import configparser
import inspect


config = configparser.ConfigParser()

# The name of config file is the name of the main script that is run with
# .ini extension
main_script_name = inspect.stack()[-1].filename.split("/")[-1].rsplit(".", 1)[0]
config.read(f'{main_script_name}.ini')

timestep = float(config['simulator']['timestep'])

bbox_size = int(config['simulator']['bbox_size'])

fig_size = int(config['simulator']['fig_size'])

dpi = int(config['simulator']['dpi'])

particles_count = int(config['simulator']['particles_count']) \
    if config.has_option('simulator', 'particles_count') else None

export_to_video = True if config['video']['export_to_video'] == 'yes' else False

filename = config['video']['filename'] \
    if config.has_option('video', 'filename') else main_script_name+".mp4"

framerate = int(config['video']['framerate'])

total_frames = int(config['video']['total_frames'])
