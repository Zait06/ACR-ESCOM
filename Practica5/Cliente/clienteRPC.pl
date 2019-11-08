use Switch;
use Try::Catch;
use Frontier::Client;

# Make an object to represent the XML-RPC server.
($HOST,$PORT)=@ARGV;
$addr=$HOST.':'.$PORT;
$server_url = 'http://'.$addr.'/RPC2';
$server = Frontier::Client->new(url => $server_url);

# Variables para el usuario, contraseña
print "Presione [M] si es que cuenta con un perfil, sino,\npresione [N] para crear una nueva cuenta: ";
$nueva=<STDIN>;
print "Usuario: "; $user=<STDIN>;
print "Contraseña: "; $pasw=<STDIN>;

$user=substr($user,0,(length($user)-1));
$pasw=substr($pasw,0,(length($pasw)-1));

if(uc($nueva)=='M'){
    $ing=$server->call(signIn,$user,$pasw);
}else{
    $ing=$server->call(logIn,$user,$pasw);
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
                case "null"     {$imprimir=$server->call(hacerPing);}
                case "create"   {$imprimir=$server->call(crearArchivo,$instruc[1],$user)}
                case "readdir"  {$imprimir=$server->call(verContenido,$user);}
                case "exit"     {$imprimir="\n\t\tHASTA PRONTO ".$user."\n"; $seguir=0;}
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

# Call the remote server and get our result.
# $result = $server->call('add',3,5);
# $sum = $result;