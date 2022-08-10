from nltk.parse.corenlp import CoreNLPServer
import os
import sys
import subprocess
java_path = "/usr/bin/java"
os.environ['JAVAHOME'] = java_path

server = CoreNLPServer(
    "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0.jar",
    "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0-models.jar"
)

if __name__ == "__main__":
    if sys.argv[1] == "start":
        server.start()
    elif sys.argv[1] == "stop":
        subprocess.call("./shutdown_server.sh", shell=True)
