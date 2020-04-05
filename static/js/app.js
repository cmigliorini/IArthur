	var fini = false;
	const updateGame = function (data) {
		
					if(!data['highlight'])
						data['highlight'] =[]
					console.log(data['highlight'])
					fini = data['fini'];
					for (let i = 0; i < 6; i++) {
						for (let j = 0; j < 7; j++) {
							var color;
							var opacity = data['highlight'].includes("("+i.toString()+", "+j.toString()+")")? "1": "0.7";
							if (data.grid[7*i+j] == 1 ){
								color = "rgb(255,255,0,"+opacity+")";
							}
							else if (data.grid[7*i+j] == 2 ){
								color = "rgb(255,  0,0,"+opacity+")";
							}
							else{
								color = "rgb(255,255,255)";
							}
							document.getElementById(getId(i,j)).style.backgroundColor = color;
						}
					}
					for(let i = 0; i < IAs.length; i++)
						document.getElementById(IAs[i]).disabled = false;
					if(data['IA'])
						document.getElementById(data['IA']).disabled= true;
					if(data['message'])
						document.getElementById("message").innerHTML = data['message'];
						
					for( i = 0; i < OrdreJeu.length; i++)
						document.getElementById(OrdreJeu[i]).disabled = false;
					if(data['futurTour']){
						document.getElementById(data['futurTour']).disabled= true;
						document.getElementById('futurTour').innerHTML= "A la prochaine partie vous jouerais en <span class='font-weight-bold'>" + data['futurTour'] +"</span>"; 
					}
					if(data['tourJoueur']){
						document.getElementById("current color").innerHTML= "Pour cette partie, vous jouez les pions <span class='font-weight-bold'>" + (data['tourJoueur'] ==  1? "jaunes" : "rouges") +"</span>"; 
						if(data['tour_de_jeu'])
							if (data['tourJoueur'] != data['tour_de_jeu'])
								waitForComputer();
					}
					
				};
	const reset = function () {
				console.log("reset");
				$.ajax({
				url: 'puissance4/ajax/reset/',
				data: {
				},
				dataType: 'json',
				success: updateGame
				});	
			};
	const waitForComputer =function () {
				console.log("wait for computer");
				document.getElementById("message").innerHTML = "En attente de l'ordinateur";
				$.ajax({
				url: 'puissance4/ajax/waitForComputer/',
				data: {
				},
				dataType: 'json',
				success: (function(data){updateGame(data);
						console.log(data['played']);
						// TODO: why && false ?
						if (data['played'] && false )
							document.getElementById(data['played']).style.backgroundColor = "yellow";
						// TODO: why && false ?
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
	const getId = function(i, j){
		return "("+String(i)+", "+String(j)+")"
	};
	
	const refresh_grid = function () {
		if (!fini) {
			console.log(this.id);
			$.ajax({
				url: 'puissance4/ajax/play/',
				data: {
					'played': this.id
				},
				dataType: 'json',
				success: (function (data) {
					updateGame(data);
					if (!fini) {
						waitForComputer();
					}
					else {
						document.getElementById("message").innerHTML = "La partie est terminée";
					}
				})
			});
		}
	};

	const refresh = function(){
		$.ajax({
					url: 'puissance4/ajax/refresh/',
					data: {
					  'played': this.id 
					},
					dataType: 'json',
					success: updateGame
					});	
		
		
	}
	const chooseIA = function(){
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
	const chooseTurn = function(){
		console.log( this.id );
		$.ajax({
		url: 'puissance4/ajax/setTour/',
		data: {
		  'tour': this.id 
		},
		dataType: 'json',
		success: (function(data) {
			for( i = 0; i < OrdreJeu.length; i++)
				document.getElementById(OrdreJeu[i]).disabled = false;
			if(data['futurTour']){
				document.getElementById(data['futurTour']).disabled= true;
				document.getElementById('futurTour').innerHTML= "A la prochaine partie vous jouerais en <span class='font-weight-bold'>" + data['futurTour'] +"</span>"; 
			}
		})
	})};

	// *** Initializations ***
	for (let i = 0; i < 6; i++) {
		for (let j = 0; j < 7; j++) {
			document.getElementById(getId(i,j)).onclick = (refresh_grid);
		}
	}
	// Set onClick behavior for active elements
	// Reset button
	document.getElementById("reset").onclick= reset;
	// Grid

	// Globals
	var IAs =["aleatoire", "basique", "simple", "dnn"]
	for(let i = 0; i < IAs.length; i++)
		document.getElementById(IAs[i]).onclick= chooseIA;
		
	var OrdreJeu =["premier", "second"]
	for(let i = 0; i < OrdreJeu.length; i++)
		document.getElementById(OrdreJeu[i]).onclick= chooseTurn;
	
	// Display initial IA setting
	chooseIA();
	refresh();