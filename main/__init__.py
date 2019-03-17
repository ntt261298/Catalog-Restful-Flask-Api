from flask import Flask

app = Flask(__name__)

# Configurations
app.config.from_object('config')
