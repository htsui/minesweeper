from pyramid.view import view_config
from .models import Board
import logging
import json

log = logging.getLogger(__name__)

#Board generation logic breaks if MINE_COUNT >= HEIGHT*WIDTH
BOARD_WIDTH=8
BOARD_HEIGHT=8
MINE_COUNT=10
boards = {}

@view_config(route_name='home', renderer='templates/index.pt')
def Home(request):
	return {}

@view_config(route_name='play', renderer='templates/play.pt')
def Play(request):
	if not (request.matchdict["room"] in boards.keys()):
		boards[request.matchdict["room"]] = Board(BOARD_WIDTH, BOARD_HEIGHT, MINE_COUNT)
	return {'BOARD_WIDTH': BOARD_WIDTH, 'BOARD_HEIGHT': BOARD_HEIGHT, 'MINES':MINE_COUNT, 'ROOM':request.matchdict["room"]}

@view_config(route_name='userInput', renderer='json')
def Respond(request):
	if not (request.matchdict["room"] in boards.keys()):
		return
	if request.json_body['type'] == 2:#reset
		boards[request.matchdict["room"]].__init__(BOARD_WIDTH,BOARD_HEIGHT,MINE_COUNT)
		return {'message': 'restart'}
	else:#type 0/1 is left/rightclick
		return {'message': boards[request.matchdict["room"]].input(request.json_body['x'],request.json_body['y'],request.json_body['type'])}

@view_config(route_name='polling', renderer='json')
def Poll(request):
	if not (request.matchdict["room"] in boards.keys()):
		return
	return {'message': boards[request.matchdict["room"]].findDifference(request.json_body['compact'])}