#!/usr/bin/python

'''

This file performs validation on session settings.

'''

from flask import current_app
from voluptuous import Schema, Required, Optional, All, Any, Coerce, In, Length


class Validator(object):
    '''

    This class provides an interface to validate the settings for each
    session.

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self, premodel_data, session_type=None):
        '''

        This constructor saves a subset of the passed-in form data.

        '''

        self.premodel_settings = premodel_data
        self.session_type = session_type

    def validate(self):
        '''

        This method validates the premodel settings for the 'data_new',
        'data_append', 'model_generate', or 'model_predict' sessions.

        Note: This method does not validate the associated 'file upload(s)',
              which is the responsibility of the mongodb query process.

        '''

        # local variables
        list_error = []
        model_type = current_app.config.get('MODEL_TYPE')
        dataset_type = current_app.config.get('DATASET_TYPE')
        sv_kernel_type = current_app.config.get('SV_KERNEL_TYPE')

        # validation on 'data_new' session
        if self.session_type == 'data_new':
            schema = Schema({
                Required('collection'): All(unicode, Length(min=1)),
                Required('dataset_type'): In(dataset_type),
                Required('model_type'): In(model_type),
                Required('session_type'): 'data_new',
                Required('session_name'): All(unicode, Length(min=1)),
                Optional('stream'): Any('True', 'False'),
            })

        # validation on 'data_append' session
        if self.session_type == 'data_append':
            schema = Schema({
                Required('collection'): All(unicode, Length(min=1)),
                Required('dataset_type'): In(dataset_type),
                Required('model_type'): In(model_type),
                Required('session_type'): 'data_append',
                Optional('stream'): Any('True', 'False'),
            })

        # validation on 'model_generate' session
        if self.session_type == 'model_generate':
            schema = Schema({
                Required('collection'): All(unicode, Length(min=1)),
                Required('model_type'): In(model_type),
                Required('session_type'): 'model_generate',
                Optional('stream'): Any('True', 'False'),
                Required('sv_kernel_type'): In(sv_kernel_type),
            })

        # validation on 'model_predict' session
        elif self.session_type == 'model_predict':
            schema = Schema({
                Required('collection'): All(unicode, Length(min=1)),
                Optional('stream'): Any('True', 'False'),
                Required('prediction_input[]'): [
                    Any(Coerce(int), Coerce(float)),
                ],
                Required('session_type'): 'model_predict',
            })

        try:
            schema(self.premodel_settings)
        except Exception, error:
            list_error.append(str(error))

        # return error
        if len(list_error) > 0:
            return {'status': False, 'error': list_error}
        else:
            return {'status': True, 'error': None}
