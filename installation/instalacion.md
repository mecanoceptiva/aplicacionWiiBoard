# Instalación

La instalación se realiza en una Raspberry Pi con Raspbian Buster.

```bash
# Dependencias
sudo apt install -y git bison flex python3-dev bluez autotools-dev automake libbluetooth-dev
# Repositorio
git clone https://github.com/azzra/python3-wiimote.git
cd python3-wiimote
# Instalación CWIID
export LC_ALL="C"
aclocal
autoconf
./configure
make
sudo make install
# Instalacion dependencias Python
cd ..
sudo apt install python3-pip libsdl1.2-dev libatlas-base-dev
sudo pip3 install pygame matplotlib
```
