from nltk.parse.corenlp import CoreNLPServer

server = CoreNLPServer(
   "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0.jar", 
   "stanford-corenlp-4.5.0/stanford-corenlp-4.5.0-models.jar"
)

server.start()