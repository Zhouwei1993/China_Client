from run import app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8877, threaded=True)
    # app.run(host="0.0.0.0",port=8877,threaded=True, ssl_context='adhoc')