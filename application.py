import logging
import logging.handlers

from wsgiref.simple_server import make_server, WSGIServer
from SocketServer import ThreadingMixIn

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/tmp/sample-app/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>Our gift to you!</head>
<style>
	body {
		color: #ffffff;
		background-color: #E0E0E0;
		font-family: Arial, sans-serif;
		font-size: 16px;
		-moz-transition-property: text-shadow;
		-moz-transition-duration: 4s;
		-webkit-transition-property: text-shadow;
		-webkit-transition-duration: 4s;
		text-shadow: none;
	}
	body.blurry {
		-moz-transition-property: text-shadow;
		-moz-transition-duration: 4s;
		-webkit-transition-property: text-shadow;
		-webkit-transition-duration: 4s;
		text-shadow: #fff 0px 0px 25px;
	}
	a {
		color: #ffffff;
	}
	.textColumn, .linksColumn {
		padding: 2em;
	}
	.textColumn {
		position: absolute;
		top: 0px;
		right: 50%;
		bottom: 0px;
		left: 0px;
		
		text-align: right;
		padding-top: 11em;
		background-color: #141414;
	}
	.textColumn p {
		width: 75%;
		float:right;
	}
	.linksColumn {
		position: absolute;
		top:0px;
		right: 0px;
		bottom: 0px;
		left: 50%;
		background-color: #A9A9A9;
	}
	
	h1 {
		font-size: 500%;
		font-weight: normal;
		margin-bottom: 0em;
	}
	h2 {
		font-size: 200%;
		font-weight: normal;
		margin-bottom: 0em;
	}
	u1 {
		padding-left: 1em;
		margin: 0px;
	}
	li {
		margin: 1em 0em;
	}
</style>
<body>
	<div class="textColumn">
		<h1>Pick a door</h1>
		<p>Our homage to Cameron</p>
	</div>
	<div class="linksColumn">
		<h2>Doors</h2>
		<ul>
			<li>
				Door
				<a href="https://team3-web-app-bucket.s3.us-west-2.amazonaws.com/duck-song-video/yt5s.com-The+Duck+Song.mp4">1</a>
			</li>
			<li>
				Door
				<a href="https://team3-web-app-bucket.s3.us-west-2.amazonaws.com/duck-song-video/yt5s.com-The+Duck+Song.mp4">2</a>
			</li>
			<li>
				Door
				<a href="https://team3-web-app-bucket.s3.us-west-2.amazonaws.com/duck-song-video/yt5s.com-The+Duck+Song.mp4">3</a>
			</li>
		</ul>
	</div>
</body>
</html>
"""

def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size)
                logger.info("Received message: %s" % request_body)
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]

class ThreadingWSGIServer(ThreadingMixIn, WSGIServer): 
    pass

if __name__ == '__main__':
    httpd = make_server('', 8000, application, ThreadingWSGIServer)
    print "Serving on port 8000..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
