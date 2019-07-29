## TFT module

# Enable SPI
sed -i 's/#dtparam=spi=on/dtparam=spi=on/' /boot/config.txt
grep -qxF 'dtoverlay=spi1-3cs' /boot/config.txt || echo 'dtoverlay=spi1-3cs' >> /boot/config.txt

# Copy FBTFT module config
cp fbtft.conf /etc/modules-load.d/

## Samba

mkdir -p "/home/pi/cave-escape-share"
if ! grep -q "# Automatically added by cave-escape-projector installer!" /etc/samba/smb.conf; then
	cp /etc/samba/smb.conf /etc/samba/smb.conf.backup
	cat smb.share.conf >> /etc/samba/smb.conf
fi

# Python

pip install -r requirements.txt

path_param=$1

chmod a+x run.py
thisdir=`pwd`
cat tftprojector.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/tft_projector.py#" \
| sed -e "s#PATH#$path_param#" \
| sed -e "s#USER#$SUDO_USER#" > tftprojector.service

systemctl enable $thisdir/tftprojector.service

