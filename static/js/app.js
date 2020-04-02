	var fini = false;
	updateGame = function (data) {
					fini = data['fini'];
					for (i = 0; i < 6; i++) {
						for (j = 0; j < 7; j++) {
							var color;
							if (data.grid[7*i+j] == 1 ){
								color = "yellow";
							}
							else if (data.grid[7*i+j] == 2 ){
								color = "red";
							}
							else{
								color = "rgba(0,0,0,0.3)";
							}
							document.getElementById(getId(i,j)).style.backgroundColor = color;
						}
					}
					for( i = 0; i < IAs.length; i++)
						document.getElementById(IAs[i]).disabled = false;
					if(data['IA'])
						document.getElementById(data['IA']).disabled= true;
				};
	reset = function () {
				console.log("reset");
				$.ajax({
				url: 'puissance4/ajax/reset/',
				data: {
				},
				dataType: 'json',
				success: updateGame
				});	
			};
	waitForComputer =function () {
				console.log("wait for computer");
				$.ajax({
				url: 'puissance4/ajax/waitForComputer/',
				data: {
				},
				dataType: 'json',
				success: (function(data){updateGame(data);
						if (!fini)
							document.getElementById("message").innerHTML = "Je viens de jouer";
						else 
							document.getElementById("message").innerHTML = "La partie est terminée";
						console.log(data['played']);
						if (data['played'] && false )
							document.getElementById(data['played']).style.backgroundColor = "yellow";
						if (data['highlight'] && false){
							var i;
							for(i = 0; i <data['highlight'].length ; i ++){
								console.log(data['highlight'])
								document.getElementById(data['highlight'][i]).style.backgroundColor = "yellow";								
							}
						}
						console.log(data['score']);
				})	
	})};
	getId = function(i, j){
		return "("+String(i)+", "+String(j)+")"
	};
	for (i = 0; i < 6; i++) {
		for (j = 0; j < 7; j++) {
			document.getElementById(getId(i,j)).onclick = (function () {
				if (!fini){
					console.log( this.id );
					$.ajax({
					url: 'puissance4/ajax/play/',
					data: {
					  'played': this.id 
					},
					dataType: 'json',
					success: (function(data) {
						updateGame(data);
						
						if (!fini){document.getElementById("message").innerHTML = "En attente de l'ordinateur";
							waitForComputer();
						}
						else{
							document.getElementById("message").innerHTML = "La partie est terminée";
						}
						})
					});	
				}
			});
		}
	}
	document.getElementById("reset").onclick= reset;
	refresh = function(){
		$.ajax({
					url: 'puissance4/ajax/refresh/',
					data: {
					  'played': this.id 
					},
					dataType: 'json',
					success: updateGame
					});	
		
		
	}
	chooseIA = function(){
		console.log( this.id );
		$.ajax({
		url: 'puissance4/ajax/setIA/',
		data: {
		  'IA': this.id 
		},
		dataType: 'json',
		success: (function(data) {
			for( i = 0; i < IAs.length; i++)
				document.getElementById(IAs[i]).disabled = false;
			if(data['IA'])
				document.getElementById(data['IA']).disabled= true;
		})
	})};
	var IAs =["aleatoire", "basique", "simple", "dnn"]
	var i;
	for( i = 0; i < IAs.length; i++)
		document.getElementById(IAs[i]).onclick= chooseIA;
	
	refresh();