# SELF SIGNED CERT
generate_ssl() {
  ip=$1
  path=ssl
  mkdir -p $path
  p=$path/
  abc='-subj "/C=DE/ST=unknown/L=unknown/O=unknown/OU=unknown/CN=unknown" -extensions v3_req'
  def="-addext \"subjectAltName = IP:$ip\""
  all="$abc $def"
  echo $all
  command="openssl req -newkey rsa:2048 -new -nodes -keyout ${p}key.pem -out ${p}csr.pem $all"
  eval $command
  command="openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout ${p}key.pem -out ${p}cert.pem $all"
  eval $command
  # https://stackoverflow.com/questions/21297139/how-do-you-sign-a-certificate-signing-request-with-your-certification-authority
  # Generate a self-signed signing certificate
  command="openssl req -x509 -days 365 -key ${p}key.pem -out ${p}ca_cert.pem $all"
  eval $command
  # Move To App
  # cp ${p}ca_cert.pem {location}cert.pem
  # Generate a certificate request
  command="openssl req -new -key ${p}key.pem -out ${p}cert_req.pem $all"
  eval $command
  # Generate a signed certificate
  command="openssl x509 -req -in ${p}cert_req.pem -days 365 -CA ${p}ca_cert.pem -CAkey ${p}key.pem -CAcreateserial -out ${p}signed_cert.pem"
  eval $command
  # Move To App
  # cp ${p}signed_cert.pem {path}
  echo done
}
generate_ssl
