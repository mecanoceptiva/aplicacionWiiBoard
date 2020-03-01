# Install CWIID

# Dependencies
sudo apt install -y git bison flex python3-dev bluez autotools-dev automake libbluetooth-dev
# Go to repo
git clone https://github.com/azzra/python3-wiimote.git
cd python3-wiimote
# Build from sources and install
export LC_ALL="C"
aclocal
autoconf
./configure
make
sudo make install
# Remove repo
cd ..
sudo rm -rf python3-wiimote
