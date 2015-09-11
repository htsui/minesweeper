from pyramid.view import view_config
from .models import Board
import logging
import json

log = logging.getLogger(__name__)

#Board generation logic breaks if MINE_COUNT >= HEIGHT*WIDTH
BOARD_WIDTH=8
BOARD_HEIGHT=8
MINE_COUNT=10

board = Board(BOARD_WIDTH, BOARD_HEIGHT, MINE_COUNT)

@view_config(route_name='home', renderer='templates/index.pt')
def MainPage(request):
	return {'BOARD_WIDTH': BOARD_WIDTH, 'BOARD_HEIGHT': BOARD_HEIGHT, 'MINES':MINE_COUNT}

@view_config(route_name='userInput', renderer='json')
def Respond(request):
	if request.json_body['type'] == 2:#reset
		board.__init__(BOARD_WIDTH,BOARD_HEIGHT,MINE_COUNT)
		return {'message': 'restart'}
	else:#type 0/1 is left/rightclick
		return {'message': board.input(request.json_body['x'],request.json_body['y'],request.json_body['type'])}

@view_config(route_name='polling', renderer='json')
def Poll(request):
	return {'message': board.findDifference(request.json_body['compact'])}
	pass