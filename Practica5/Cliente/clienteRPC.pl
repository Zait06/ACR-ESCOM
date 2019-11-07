use Try::Catch;
use Frontier::Client;

# Make an object to represent the XML-RPC server.
($HOST,$PORT)=@ARGV;
$addr=$HOST.':'.$PORT;
$server_url = 'http://'.$addr.'/RPC2';
$server = Frontier::Client->new(url => $server_url);
# Variables para el usuario, contraseña
print "Presione [M] si es que cuenta con un perfil, sino,\nprecione [N] para crear una nueva cuenta: ";
$nueva=<STDIN>;
print "Usuario: "; $user=<STDIN>;
print "Contraseña: "; $pasw=<STDIN>;

if(uc($nueva)=='M'){
    $ing=$server->call(signIn,$user,$pasw);
}else{
    $ing=$server->call(logIn,$user,$pasw);
}

$seguir=1;
if($ing){
    print "\tSesión iniciada\n";
    while($seguir){
        $imprimir='';
        print "\nuser@".$user.">> "; 
        $orden=<STDIN>;
        @instruc=split(' ',lc($orden));
        try{
            if($instruc[0]=='null'){
                $imprimir=$server->call(hacerPing);
            }elsif($instruc[0]=='create'){
                $imprimir=$server->call(crearArchivo,$instruc[1],$user);
            }elsif($instruc[0]=='read'){
                $imprimir=$server->call(leerArchivo,$user,$instruc[1]);
            }elsif($instruc[0]=='exit'){
                $imprimir="Saliendo";
                $seguir=0;
            }else{
                $imprimir="Instruccion incorrecta, intente de nuevo\n";
            }
            print($imprimir);
        }catch(e){ 
            print("Exception: " $e);
        }
        
    }
}else{
    print "Usuario o contraseña incorrectas";
}

# Call the remote server and get our result.
# $result = $server->call('add',3,5);
# $sum = $result;