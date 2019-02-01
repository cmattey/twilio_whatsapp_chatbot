from flask import Flask

app = Flask(__name__) # __name__ is a Python pre defined variable, which is socket
# to the name of the module in which it is used.

from chatbot import routes # this import statement is added at the end in order
# to avoid a circular dependency
