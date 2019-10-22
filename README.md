# nerver-tancredi

This package download last version of tancredi and package it for NethServer.

It is intended to be used with travis-ci, to build it manually launch: ::

    ./get_tancredi.sh
    mkdir tancredi
    tar xzpf tancredi-vendor.tar.gz -C tancredi --strip-components 1
    cd tancredi
    curl -sS https://getcomposer.org/installer | php
    php composer.phar install
    cd ..
    tar czpf tancredi.tar.gz tancredi

Than make package as usual: ::

   rm *.rpm; export dist=ns7;export mockcfg=nethserver-7-x86_64; make-rpms *.spec; ls *.rpm 
 

