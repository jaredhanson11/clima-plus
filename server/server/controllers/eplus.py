from flask import request, send_from_directory
from flask_restful import Resource
from werkzeug import secure_filename
from uuid import uuid4
import os
import subprocess

from ..utils import responses
from .. import config

class SimulationController(Resource):
    def get(self, uuid):
        '''
        Gets results of simulation, if available.
        '''
        simulation_folder = os.path.join(config.EPLUS_SIMULATION_FOLDER, uuid + '/')
        output_pn = os.path.join(simulation_folder, 'eplusout.csv')
        if os.path.isfile(output_pn):
            return send_from_directory(simulation_folder, 'eplusout.csv', as_attachment=True)
            ## USUALLY YOU SEND responses.success({'file_location': <url_to_file>})
            ## I'm only not because its a local example
        else:
            return responses.error({'errMsg': 'Simulation not available'})


    def post(self):
        '''
        Runs simulation for uploaded idf and returns address of results.
        '''
        if 'idf' not in request.files:
            return responses.error({'errMsg': 'idf file not provided.'})
        idf_upload = request.files['idf']
        simulation_id = str(uuid4())
        print config

        simulation_folder = os.path.join(config.EPLUS_SIMULATION_FOLDER, simulation_id + '/')
        simulation_idf_fn = secure_filename('in.idf')
        simulation_idf_fp = os.path.join(simulation_folder, simulation_idf_fn)
        expanded_idf_fp = os.path.join(simulation_folder, 'expanded.idf')
        os.makedirs(simulation_folder)
        idf_upload.save(simulation_idf_fp)
        expand_objects = subprocess.Popen(['/usr/local/bin/ExpandObjects'], cwd=simulation_folder)
        expand_objects.wait()
        subprocess.Popen(' '.join(['/usr/local/bin/energyplus', '-w', config.EPW_FILE_LOCATION, '-d', simulation_folder, expanded_idf_fp, ';', '/usr/local/bin/ReadVarsESO']), shell=True, cwd=simulation_folder)
        return responses.success({'simulation_id': simulation_id})
