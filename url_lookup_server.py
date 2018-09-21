import configparser
from flask import Flask
from flask import request, jsonify
from db_operations import DBOperations

config = configparser.ConfigParser()
config.read("config.ini")
app = Flask(__name__)

# Creating database connection at the start of the API server.
db = DBOperations(config["mysql"]["host"], config["mysql"]["port"],
                  config["mysql"]["user"], config["mysql"]["password"])
db_connection = db.connect(config["mysql"]["db"])


class ResponseMessage(Exception):
    """ Defining our own exception class to pass sensible response messages """
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(ResponseMessage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/", methods=["GET"])
def home_page():
    """ To display Home page """
    app.logger.debug("Displaying home page !!")
    return "Welcome to URL lookup service !!"


@app.route("/api/v1/check/url", methods=["GET"])
def check_url():
    """ To parse the URL and
    compare the requested URL with the ones stored in DB """
    global db_connection
    result = dict()
    result["type"] = "Normal"
    if "url" in request.args:
        url = request.args["url"]
        if len(url) > 2000:
            # return 414 (Request-URI too long) status code.
            msg = "URL requested is too long."
            app.logger.error(msg)
            raise ResponseMessage(msg, status_code=414, payload={"url": url})
        if not url:
            # return 400 (Bad request) status code.
            msg = "URL value is missing."
            app.logger.error(msg)
            raise ResponseMessage(msg, status_code=400, payload={"url": url})
        result["url"] = url
    else:
        # return 400 (Bad request) status code.
        msg = "No url field provided. Please specify an url."
        app.logger.error(msg)
        raise ResponseMessage(msg, status_code=400)

    if not db_connection:
        # return 500 (Server error) status code.
        msg = "Connection to database failed."
        app.logger.error(msg)
        raise ResponseMessage(msg, status_code=500, payload={"url": url})

    sql_query = "select * from {}".format(config["mysql"]["table"])
    query_res = db.execute(db_connection, sql_query)
    if not query_res:
        # return 500 (Server error) status code.
        msg = "Failed to retrieve data from database."
        app.logger.error(msg)
        raise ResponseMessage(msg, status_code=500, payload={"url": url})

    app.logger.debug("Result from MySQL : {}".format(query_res))
    for row in query_res:
        if url in row:
            result["type"] = "Malware"
            # return 200 (Success/Ok) status code.
            msg = "Requested URL is a malware."
            app.logger.error(msg)
            raise ResponseMessage(msg, status_code=200, payload=result)

    # return 200 (Success/Ok) status code.
    msg = "Requested URL is not a malware."
    app.logger.debug(msg)
    raise ResponseMessage(msg, status_code=200, payload=result)


if __name__ == "__main__":
    app.run(host=config["default"]["service_ip"],
            port=config["default"]["service_port"],
            debug=config["default"]["service_log_debug"])
