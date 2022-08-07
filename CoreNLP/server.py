from nltk.parse.corenlp import CoreNLPServer
import os
java_path = "D:/jdk-17.0.0.35-hotspot/bin/java.exe"
os.environ['JAVAHOME'] = java_path

server = CoreNLPServer(
   "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0.jar", 
   "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0-models.jar"
)

server.start()