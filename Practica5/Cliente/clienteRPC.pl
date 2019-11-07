use Frontier::Client;

# Make an object to represent the XML-RPC server.
($HOST,$PORT)=@ARGV;
print "$HOST"; print "$PORT\n";
$server_url = 'http://127.0.0.1:8080/RPC2';
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

if($ing){
    print "Si jala"
}else{
    print "Usuario o contraseña incorrectas"
}

# Call the remote server and get our result.
# $result = $server->call('add',3,5);
# $sum = $result;