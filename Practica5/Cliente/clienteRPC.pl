use Switch;
use Try::Catch;
use Frontier::Client;

($HOST,$PORT)=@ARGV;                                    # IP y puerto del servidor
$addr=$HOST.':'.$PORT;                                  # Dirección del servidor
$server_url = 'http://'.$addr.'/RPC2';                  # Protocolo, direccion, carpeta del servidor
$server = Frontier::Client->new(url => $server_url);    # Conexión del servidor

# Variables para el usuario, contraseña
print("\tSERVICIO RPC")
print "Presione [M] si es que cuenta con un perfil, sino,\npresione [N] para crear una nueva cuenta: ";
$nueva=<STDIN>;
print "Usuario: "; $user=<STDIN>;
print "Contraseña: "; $pasw=<STDIN>;

$user=substr($user,0,(length($user)-1));    # usuario sin '\n'
$pasw=substr($pasw,0,(length($pasw)-1));    # contraseña sin '\n'

if(uc($nueva)=="M"){
    $ing=$server->call(signIn,$user,$pasw); # Ingresar con un perfil
}else{
    $ing=$server->call(logIn,$user,$pasw);  # Crear un perfil
}

$seguir=1;
if($ing){
    print "\tSesión iniciada\n";
    while($seguir){
        $imprimir="";
        print "\nuser@".$user.">> "; 
        $orden=<STDIN>;
        @instruc=split(' ',lc($orden));
        try{
            switch($instruc[0]){
                case "null"     {$imprimir=$server->call(hacerPing);}                               # Hace un ping con el servidor
                case "create"   {$imprimir=$server->call(crearArchivo,$instruc[1],$user);}          # Crea un archivo
                case "lookup"   {$imprimir=$server->call(ordenLookUp,$user,$instruc[1]);}           # Busca un archivo o directorio
                case "read"     {$imprimir=$server->call(leerArchivo,$user,$instruc[1]);}           # Lee un archivo
                case "write"    {                                                                   # Edita un archivo
                                    print "Ingrese un texto:\n->";
                                    $dato=<STDIN>;
                                    $dato=substr($dato,0,(length($dato)-1));
                                    $imprimir=$server->call(editarArchivo,$user,$instruc[1],$dato);
                                }
                case "rename"   {$imprimir=$server->call(renombrar,$instruc[1],$instruc[2],$user);} # Cambia el nombre al archivo
                case "remove"   {$imprimir=$server->call(borrarArchivo,$instruc[1],$user);}         # Elimina un archivo
                case "mkdir"    {$imprimir=$server->call(crearCarpeta,$instruc[1],$user);}          # Crea un directorio
                case "rmdir"    {$imprimir=$server->call(borrarCarpeta,$instruc[1],$user);}         # Elimina un directorio
                case "readdir"  {$imprimir=$server->call(verContenido,$user);}                      # Vista de todos los archivos
                case "getattr"  {$imprimir=$server->call(infoArchivo,$instruc[1],$user);}           # Informacion del archivo
                case "access"   {$imprimir=$server->call(accesoPath,$user);}                        # Acceso del usuario
                case "pwd"      {$imprimir=$server->call(verDireccion,$user);}                      # Direccion del usuario
                case "help"     {$imprimir=$server->call(ayudame);}                                 # Lista de comandos
                case "?"        {$imprimir=$server->call(ayudame);}                                 # Lista de comandos
                case "exit"     {$imprimir="\n\t\tHASTA PRONTO ".$user."\n"; $seguir=0;}            # Salir de todo
                else            {$imprimir="Instruccion incorrecta, intente de nuevo\n";}
            }
            print($imprimir);
        }catch{ 
            warn "Algo anda mal...";
        }
        
    }
}else{
    print "Usuario o contraseña incorrectas";
}