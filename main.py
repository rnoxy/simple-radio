# mypy-radio is a simple internet radio player written in Python.
#
# This is very simple application that is using the VLC library to play the internet radio stations.
# This application is listening on the port 5017 and can be accessed using REST API.

import os
import yaml
import vlc
from flask import Flask, request, jsonify

URL = os.environ.get("MYPY_RADIO_URL", "0.0.0.0")
PORT = os.environ.get("MYPY_RADIO_PORT", 5017)


# Player class that is responsible for playing the music.
class Player:
    def __init__(self, config_file: str = "config.yml"):
        self.radio_stations = self.load_radio_stations(config_file)
        self.current_station_id = 0
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    # load the radio stations from the config file
    def load_radio_stations(self, config_file: str) -> list[dict]:
        with open(config_file) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @property
    def current_station_name(self):
        return self.radio_stations[self.current_station_id]["name"]

    @property
    def current_station_url(self):
        return self.radio_stations[self.current_station_id]["url"]

    # play the current radio station
    def play(self):
        print("Playing: " + self.current_station_name)
        media = self.instance.media_new(self.current_station_url)
        self.player.set_media(media)
        self.player.play()

    # switch to the next radio station
    def next(self):
        self.current_station_id = (self.current_station_id + 1) % len(
            self.radio_stations
        )
        self.play()

    # switch to the previous radio station
    def previous(self):
        self.current_station_id = (self.current_station_id - 1) % len(
            self.radio_stations
        )
        self.play()


app = Flask(__name__)
player = Player()


# this is the main route of the application
@app.route("/")
def index():
    return "Hello, World!"


# this is the route that is responsible for getting the list of the internet radio stations
@app.route("/get_radio_stations", methods=["GET"])
def get_radio_stations():
    return jsonify(player.radio_stations)


# this is the route that is responsible for getting the current radio station
@app.route("/get_current_radio_station", methods=["GET"])
def get_current_radio_station():
    return jsonify(player.current_station_name)


# this is the route that is responsible for playing the current radio station
@app.route("/play", methods=["GET"])
def play():
    player.play()
    return jsonify(player.current_station_name)


# this is the route that is responsible for switching to the next radio station
@app.route("/next", methods=["GET"])
def next():
    player.next()
    return jsonify(player.current_station_name)


# this is the route that is responsible for switching to the previous radio station
@app.route("/prev", methods=["GET"])
def previous():
    player.previous()
    return jsonify(player.current_station_name)


# this is the route that is responsible for playing the specific radio station
@app.route("/play/<int:station_id>", methods=["GET"])
def play_station(station_id: int):
    player.current_station_id = station_id
    player.play()
    return jsonify(player.current_station_name)


# this is the route that is responsible for stopping the current radio station
@app.route("/stop", methods=["GET"])
def stop():
    player.player.stop()
    return jsonify("Stopped")


if __name__ == "__main__":
    # run the application
    player.play()
    app.run(host=URL, port=PORT)
