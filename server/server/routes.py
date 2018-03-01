from . import api
#import controllers.sample
import controllers.eplus

def add_routes():
    api.add_resource(controllers.eplus.SimulationController, '/simulate/<string:uuid>')
    #api.add_resource(controllers.sample.SampleController, '/')
