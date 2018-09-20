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
        # return 414 (Request-URI too long) status code.
        if len(url) > 2000:
            return jsonify(result)
        result["url"] = url
    else:
        app.logger.error("No url field provided. Please specify an url.")
        # return 400 (Bad request) status code.
        return jsonify(result)

    if not db_connection:
        # return 500 (Server error) status code.
        return jsonify(result)

    sql_query = "select * from {}".format(config["mysql"]["table"])
    query_res = db.execute(db_connection, sql_query)
    if not query_res:
        # return 500 (Server error) status code.
        return jsonify(result)
    app.logger.debug("Result from MySQL : {}".format(query_res))
    for row in query_res:
        if url in row:
            result["type"] = "Malware"
            app.logger.error("Requested URL is a malware !!")
            break

    # return 200 (Success/Ok) status code.
    return jsonify(result)


if __name__ == "__main__":
    app.run(host=config["default"]["service_ip"],
            port=config["default"]["service_port"],
            debug=config["default"]["service_log_debug"])
    # TODO: Add code to close DB connection once the app is stopped.
