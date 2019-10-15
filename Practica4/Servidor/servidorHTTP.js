var http=require("http"),  // Protocolo
	fs=require("fs");	// Lector de archivos

var peticion=function(solicitud,respuesta){	// Función de la respuesta
	console.log("Solicitud pedida");	// Solicitud al servidor
	fs.readFile("./pagina.html",function(err,html){
		respuesta.write(html);	// Lectura de HTML
		respuesta.end();
	})
};

var servidor=http.createServer(peticion); // Crea servidor

servidor.listen(8080);	// Puerto habilitado