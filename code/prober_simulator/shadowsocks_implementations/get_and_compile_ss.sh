#!/bin/bash

sudo -v

function compile {
    version="$1"

    sudo cp -r "shadowsocks-libev" "shadowsocks-libev_${version}"
    cd "shadowsocks-libev_${version}"

    sudo git clean  -d  -f .
    sudo git checkout -f "${version}"

    #git reset --hard origin/master
    #git pull
    ####sudo git submodule init && git submodule update
    #cp -r ../libsodium-1.0.16 .
    #cp -r ../mbedtls-2.6.0 .
    #sudo ldconfig

    # Start building
    ./autogen.sh && ./configure && make
    sudo make install

    cd ..

    mkdir "compiled_binary_${version}"
    cd "compiled_binary_${version}"
    sudo mv /usr/local/bin/ss-server .
    sudo mv /usr/local/bin/ss-local .
    cd ..
}

# https://github.com/shadowsocks/shadowsocks-libev/tags
# failed: v2.5.6, v2.4.8, v2.3.3
#VERSIONS=('v3.3.3' 'v3.2.5' 'v3.1.3' 'v3.0.8' 'v2.6.3' 'v2.5.6' 'v2.4.8' 'v2.3.3' 'v2.2.3' 'v2.1.4' 'v2.0.8' 'v1.6.4' 'v1.5.3' 'v1.4.8')
#VERSIONS=('v3.3.1' 'v2.2.3' 'v2.1.4' 'v2.0.8' 'v1.6.4' 'v1.5.3' 'v1.4.8')
VERSIONS=('v3.2.0')

for version in "${VERSIONS[@]}"; do
  echo "Method: $version"
  compile "$version"
done

