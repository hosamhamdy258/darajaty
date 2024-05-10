bind = "0.0.0.0:9000"
workers = 3
loglevel = "info"
pythonpath = "/app"
wsgi_app = "core.wsgi:application"

# accesslog = "./logger/access.log"
# errorlog = "./logger/error.log"
capture_output = True

reload = True
