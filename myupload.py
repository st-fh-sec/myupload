from flask import Flask, render_template, request, send_from_directory, redirect
import os.path
from werkzeug import secure_filename
import re
import os
import logging

app = Flask(__name__, template_folder='templates')

logger = logging.getLogger('upload')
#hdlr = logging.FileHandler('app.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


def check_token(token):
   if re.search('[0-9]+', token):
     return True 
   else:
     logger.error('request token has invalid format')
     return False

@app.route('/folder', methods = ['GET'])
def view_folder():
   logger.debug('view folder')
   token = request.args['token']

   if not check_token(token):
      return render_template('msg.html', title='token not valid')

   target_dir = os.path.join('uploads', token)
   if not os.path.exists(target_dir):
      logger.error('request token is not present')
      return render_template('msg.html', title='token not found')

   files = []
   for root, dirnames, filenames in os.walk(target_dir):
      for filename in filenames:
          files.append(filename)
   
   return render_template('folder.html', files=files, token=token)
   
@app.route('/download', methods = ['GET'])
def download_file():
   logger.debug('download file')
   token = request.args['token']
   filename = request.args['file']
   target_dir = os.path.join('uploads', token)

   return send_from_directory(directory=target_dir, filename=filename) #, as_attachment=True)

@app.route('/upload', methods = ['GET','POST'])
def upload_file():
   logger.debug('new request')

   if not 'token' in request.args:
      logger.error('request has no token')
      return render_template('msg.html', title='bad request')
   token = request.args['token']

   if not check_token(token):
      return render_template('msg.html', title='token not valid')

   target_dir = os.path.join('uploads', token)
   if not os.path.exists(target_dir):
      logger.error('request token is not present')
      return render_template('msg.html', title='token not found')

   if request.method == 'POST':
      logger.debug('post request')
      f = request.files['file']
      target_file = os.path.join(target_dir, secure_filename(f.filename))
      logger.debug('target file = {0}'.format(target_file))
      # TODO file size checks
      f.save(target_file)
      logger.info('file {0} written to file system'.format(target_file))
      return redirect('/folder?token=' + token, code=302)

   else:
      logger.debug('get request')
      return render_template('upload.html', title='upload file')
		
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug = True)
