from flask import request
from flask_restful import Resource
from werkzeug import secure_filename
from uuid import uuid4

from ..utils import responses
from .. import config

class SimulationController(Resource):
    def post(self):
        '''
        Runs simulation for uploaded idf and returns address of results.
        '''
        if 'idf' not in request.files:
            return responses.error({'errMsg': 'idf file not provided.'})
        idf_upload = request.files['idf']
        simulation_id = str(uuid4())
        simulation_idf_fn = simulation_id + '.idf'
        filename = secure_filename(simulation_idf_fn)
        idf_upload.save(os.path.join(config.EPLUS_IDF_UPLOAD_FOLDER, simulation_idf_fn))
        return responses.success({'simulation_id': simulation_id})
