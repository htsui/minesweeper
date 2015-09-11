$(document).ready(function(){
	var WIN_MESSAGE = "You've won!  Play again by clicking the restart button"
	var LOSE_MESSAGE = "You hit a mine.  Click the restart button to try again."
	var RESTART_MESSAGE = "Another player has restarted the game"
	var POLLING_RATE = 500;

	var revealed = 0;
	var elems = []
	
	init()
	start()
	poll()
	/*
		Click Listeners
	*/
	$("table").on("click", "td", function(){
		ajax_request($(this).data('x'), $(this).data('y'),0)
	});

	$("table").on("contextmenu", "td", function(){
		ajax_request($(this).data('x'), $(this).data('y'),1)
		return false;
	});
	$("#restart").click(function(){
		ajax_request(0,0,2);
	});

	/*
		Initialization Code
	*/
	function init(){
		for(var i = 0; i < BOARD_WIDTH; i++){
			var row = []
			for (var j = 0; j < BOARD_HEIGHT; j++){
				var elem = $('td[data-x='+i+'][data-y='+j+']')
				row.push(elem);
			}
			elems.push(row);
		}
	}

	function start(){
		revealed = 0;
		for (var i = 0; i < BOARD_HEIGHT; i++){
			for (var j = 0; j < BOARD_WIDTH; j++){
				clearSquare(j,i);
			}
		}
	}
	/*
		What to do with AJAX responses?
	*/
	function processAjax(data){
		if (data.message == null){
		} else if (data.message == 'restart'){
			$('td').attr('class','').html('');
			start();
		} else {
			for (var i = 0; i < data.message.length; i++){
				updateSquare(data.message[i]);
			}
		}
	}
	/*
		Server has given us coordinates and data, update to reflect it on the UI
		"square" is server data, being compared with client accessors "isVisibleNumber", "isVisibleMine", etc
	*/
	function updateSquare(square){
		if (square==null){
			return;
		}
	    var x = square.coords[0]
	    var y = square.coords[1]

	    /*Conditions that signify a restart occured*/
	    /*Maybe I should have tried to figure out websockets instead...*/
	    if ((square.isFlag && (isVisibleNumber(x,y) || isVisibleMine(x,y)))
	    	|| (!square.isVisible && !square.isFlag && (isVisibleNumber(x,y) || isVisibleMine(x,y)))
	    	|| (square.isVisible && !square.isMine && isVisibleMine(x,y))
	    	|| (square.isVisible && square.isMine && isVisibleNumber(x,y))
	    	|| (square.isVisible && !square.isMine && isVisibleNumber(x,y) && !doNumbersMatch(x,y,square))){
	    		restartGame()
	    	} else {
	    		/*If a restart did not occur, just update the board and play on*/
	    		if (square.isFlag){
	    			showFlag(x,y)
	    		} else if (square.isMine){
	    			showMine(x,y)
	    		} else if (square.isVisible){
	    			if (!isVisibleNumber(x,y))
	    				showNumber(x,y,square.touchingMines)
	    		} else {
	    			hideFlag(x,y)
	    		}
	    	}
	}
	/*
		Helper functions for board update
	*/
	function isFlag(x,y){
		return elems[x][y].hasClass("flag")
	}
	function isVisibleMine(x,y){
		return elems[x][y].hasClass("mine")
	}
	function doNumbersMatch(x,y,square){
		return (elems[x][y].html() == (square.touchingMines == 0 ? " " : square.touchingMines))
	}
	function isVisibleNumber(x,y){
		return elems[x][y].html() != ""
	}
	function showMine(x,y){
		elems[x][y].attr("class","mine");
		alert(LOSE_MESSAGE);
	}
	function showNumber(x,y,numberOfMines){
		console.log(x+","+y)
		elems[x][y].html(numberOfMines == 0 ? " " : numberOfMines);
		elems[x][y].attr("class","revealed");
		revealed++;
		if (revealed == BOARD_WIDTH*BOARD_HEIGHT - MINES){
			console.log(revealed)
			console.log(BOARD_HEIGHT*BOARD_WIDTH)
			console.log(MINES)
			alert(WIN_MESSAGE);
		}
		console.log(revealed)
	}
	function showFlag(x,y){
		elems[x][y].attr("class","flag");
	}
	function hideFlag(x,y){
		elems[x][y].attr("class","");
	}
	function clearSquare(x,y){
		elems[x][y].empty();
		elems[x][y].attr("class","");
	}
	function restartGame(){
		alert(RESTART_MESSAGE);
		start()
	}

	/*
	Polling/multiplayer code
	*/
	function poll(){
		jQuery.ajax({
			url     : 'polling',
			type    : 'POST',
			data: JSON.stringify({'compact': compactify()}),
			contentType: 'application/json; charset=utf-8',
			success : function(data){
				processAjax(data);
				setTimeout(poll,POLLING_RATE);
			},
			error : function(){
				console.log("Connection Error... trying again");
				setTimeout(poll,POLLING_RATE);
			}
		});
	}

	/*Create a string representing the grid to save bandwidth on polling*/
	/*For more efficiency, store in binary!  4bits/square is enough, 0-8 and F,M,N is < 2^4 possibilities*/
	function compactify(){
		var str = "";
		for (var i = 0; i < BOARD_WIDTH; i++){
			for (var j = 0; j < BOARD_HEIGHT; j++){
				if (isFlag(i,j))
					str += "F"
				else if (isVisibleMine(i,j))
					str += "M"
				else if (isVisibleNumber(i,j))
					str += elems[i][j].html() == " " ? 0 : elems[i][j].html()
				else
					str += "N"//None
			}
		}
		console.log(str);
		return str;
	}
	/*
	AJAX function
	*/
	function ajax_request(x,y,type){//type 0 = click, 1 = flag, 2 = restartgame
		jQuery.ajax({
			url     : 'play',
			type    : 'POST',
			data: JSON.stringify({'x': x, 'y': y, 'type':type}),
			contentType: 'application/json; charset=utf-8',
			success : function(data){
				if (data != null){
					processAjax(data);
				}
			}
		});
	}
});

