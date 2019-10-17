var http=require("http"),  // Protocolo
	fs=require("fs");	// Lector de archivos

var peticion=function(solicitud,respuesta){	// Función de la respuesta
	console.log("Solicitud pedida con el metodo %s",solicitud['method']);	// Solicitud al servidor
	console.log(solicitud['headers'])
	fs.readFile("./pagina.html",function(err,html){
		var html_str=html.toString();
		respuesta.write("Tarea hecha");	// Lectura de HTML
		respuesta.end();
	})
};

console.log("Servidor a la escucha")

var servidor=http.createServer(peticion); // Crea servidor

servidor.listen(8080);	// Puerto habilitado