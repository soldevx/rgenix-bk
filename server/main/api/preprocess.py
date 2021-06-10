# -*- coding: utf-8 -*-
'''User Route for application.'''

from server.main.models.cvs import CV
from server.main.models.jobdescs import Jobdesc
from server.main.services.preprocess_service import CVService, JobdescService
from server.main.ml.ranker import preprocess

from io import BufferedReader
from flask import Blueprint, request

route = Blueprint('user', __name__)

jobdes = JobdescService()
cv = CVService()

@route.route('/api/preprocess', methods=['POST'])
def api_preprocess():
    uid = request.args.get('uid')
    prep_type = request.args.get('type')
    pdf_file = BufferedReader(request.files['file'])
    tfidf, word2vec = preprocess(pdf_file)
    if prep_type == 'cv':
        jid = request.args.get('jid')
        _cv = CV(tfidf, word2vec, uid, jid)
        CVService().save(_cv)
    elif prep_type == 'jobdesc':
        _jobdesc = Jobdesc(pdf_file, tfidf, str(word2vec), uid)
        JobdescService().save(_jobdesc)
    else:
        raise ValueError(f'Invalid document type, got {prep_type}')
    return 'Success'