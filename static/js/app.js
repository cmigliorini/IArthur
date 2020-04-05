	var fini = false;
	updateGame = function (data) {
		
					if(!data['highlight'])
						data['highlight'] =[]
					console.log(data['highlight'])
					fini = data['fini'];
					for (i = 0; i < 6; i++) {
						for (j = 0; j < 7; j++) {
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
					for( i = 0; i < IAs.length; i++)
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
				document.getElementById("message").innerHTML = "En attente de l'ordinateur";
				$.ajax({
				url: 'puissance4/ajax/waitForComputer/',
				data: {
				},
				dataType: 'json',
				success: (function(data){updateGame(data);
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
						
						if (!fini){
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
	chooseTurn = function(){
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
	var IAs =["aleatoire", "basique", "simple", "dnn"]
	var i;
	for( i = 0; i < IAs.length; i++)
		document.getElementById(IAs[i]).onclick= chooseIA;
		
	var OrdreJeu =["premier", "second"]
	for( i = 0; i < OrdreJeu.length; i++)
		document.getElementById(OrdreJeu[i]).onclick= chooseTurn;
	
	// Initialize buttons
	chooseIA(null);
	refresh();