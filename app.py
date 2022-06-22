import pyglet
from pyglet import shapes
from enviroment import Enviroment, Configuration

Scale = 6

my_configuration = Configuration()
my_configuration.inputs = ['input_distance_left', 'input_distance_right']
my_configuration.outputs = ['vertical_movement', 'horizontal_movement']
my_configuration.middle = 2
my_configuration.genome_size = 8
my_configuration.mutation = 0.5
my_configuration.enviroment_size = (100, 100)
my_configuration.enviroment_lifespan = 100
my_configuration.population_size = 80
my_configuration.elimination_function = 'elimination_sides'

my_env = Enviroment(my_configuration)
my_env.generate()

my_batch = pyglet.graphics.Batch()
window = pyglet.window.Window(600, 600)

alive = []

def update(dt):
    global alive
    if not my_env.alive:
        my_env.eliminate()
        my_env.generate()
    alive = []
    for graph in my_env.simulate():
        new_rectangle = shapes.Rectangle(graph['position'][0] * Scale,
                                         graph['position'][1] * Scale,
                                         Scale, Scale,
                                         color=graph['color'],
                                         batch=my_batch)
        alive.append(new_rectangle)

pyglet.clock.schedule_interval(update, 1/30)

@window.event
def on_draw():
    update(0)
    window.clear()
    my_batch.draw()

pyglet.app.run()