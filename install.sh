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

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

chmod a+x run.py
chmod a+x run_public.sh
chmod a+x run_local.sh

thisdir=`pwd`
cat tftprojector.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/run_public.sh#" \
| sed -e "s#USER#$SUDO_USER#" > tftprojector.service

systemctl enable $thisdir/tftprojector.service
