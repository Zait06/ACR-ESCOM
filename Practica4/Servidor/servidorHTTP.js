var http=require("http"),  // Protocolo
	fs=require("fs");	// Lector de archivos

var peticion=function(solicitud,respuesta){	// Función de la respuesta
	console.log("Solicitud pedida con el metodo %s",solicitud['method']);	// Solicitud al servidor
	//console.log(solicitud)
	fs.readFile("./pagina.html",function(err,html){
		var html_str=html.toString();
		var variables=html_str.match(/[^\{\}]+(?=\})/g);
		// respuesta.writeHead(200,{'Content-Type':'text/html'})
		respuesta.write(html_str);	// Lectura de HTML
		respuesta.end();
	})
};

var servidor=http.createServer(peticion); // Crea servidor

servidor.listen(8080);	// Puerto habilitado