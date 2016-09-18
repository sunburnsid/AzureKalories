from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from clarifai.client import ClarifaiApi
import os
import tempfile
import base64
import random, string

clarifai_api = ClarifaiApi("Sa3eWiFzsFVygnleCNQAPvJacvIVAvkBBbN5cxmY", "qIf-5HaEzO225zuUaj5FTREU7iYAJLHU5_XrpHH_") # assumes environment variables are set.
result = clarifai_api.tag_images(open('cheese.jpg', 'rb'))
print ("api call")
#result = {u'status_code': u'OK', u'status_msg': u'All images in request have completed successfully. ', u'meta': {u'tag': {u'timestamp': 1474084104.627829, u'model': u'general-v1.3', u'config': None}}, u'results': [{u'docid': 42024272502422257284519421165328554557L, u'status_code': u'OK', u'status_msg': u'OK', u'local_id': u'', u'result': {u'tag': {u'classes': [u'carrot', u'root', u'food', u'no person', u'provitamin A', u'vegetable', u'nutrition', u'health', u'healthy', u'agriculture', u'diet', u'leaf', u'desktop', u'freshness', u'grow', u'close-up', u'juicy', u'bunch', u'ingredients', u'cooking'], u'concept_ids': [u'ai_DGvpjM5g', u'ai_3xJvggfW', u'ai_3PlgVmlN', u'ai_786Zr311', u'ai_grVmTvp7', u'ai_LpcgM7r5', u'ai_nl2sV1Hm', u'ai_mZ2tl6cW', u'ai_0mCQLwrm', u'ai_ZsprRgCn', u'ai_Cp0N9mF9', u'ai_wBCrHPDb', u'ai_Lq00FggW', u'ai_mZJ4nprg', u'ai_VRrpDkps', u'ai_4lvjn8qv', u'ai_gt6djlDq', u'ai_mXdcXbrT', u'ai_xzqBDlmV', u'ai_KXNqVd5F'], u'probs': [0.9975664615631104, 0.9955800175666809, 0.9922435283660889, 0.99013352394104, 0.9898305535316467, 0.9868329763412476, 0.9771294593811035, 0.9762943983078003, 0.9708182215690613, 0.9601856470108032, 0.956566572189331, 0.9558433294296265, 0.9373021125793457, 0.9226887226104736, 0.9224319458007812, 0.9132283329963684, 0.911675214767456, 0.9096507430076599, 0.9050804972648621, 0.8930140733718872]}}, u'docid_str': u'1f9d949a5c38fffe3e7e2f58c7ca5a3d'}]}
parsed = result['results'][0]['result']['tag']['classes']
answer = []
print (parsed)
for val in parsed:
    print (val)
