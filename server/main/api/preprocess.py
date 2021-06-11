# -*- coding: utf-8 -*-
'''User Route for application.'''

from server.main.models.cvs import CV
from server.main.models.jobdescs import Jobdesc
from server.main.services.preprocess_service import CVService, JobdescService
from server.main.ml.ranker import preprocess

from io import BufferedReader
from flask import Blueprint, request

route = Blueprint('preprocess', __name__)

jobdesc_service = JobdescService()
cv_service = CVService()

@route.route('/api/preprocess', methods=['POST'])
def api_preprocess():
    uid = request.args.get('uid')
    prep_type = request.args.get('type')
    pdf_file = BufferedReader(request.files['file'])
    tfidf, word2vec = preprocess(pdf_file)
    pdf_file = pdf_file.read()
    if prep_type == 'cv':
        jid = request.args.get('jid')
        _cv = CV(pdf_file, tfidf, word2vec, uid, jid)
        cv_service.save(_cv)
    elif prep_type == 'jobdesc':
        _jobdesc = Jobdesc(pdf_file, tfidf, str(word2vec), uid)
        jobdesc_service.save(_jobdesc)
    else:
        raise ValueError(f'Invalid document type, got {prep_type}')
    return 'Success'