from . import api
#import controllers.sample
import controllers.eplus

def add_routes():
    api.add_resource(controllers.eplus.SimulationController, '/simulate')
    #api.add_resource(controllers.sample.SampleController, '/')
