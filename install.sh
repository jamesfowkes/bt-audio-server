## TFT module

## Samba

mkdir -p "/home/pi/bt-audio-server-share"
if ! grep -q "# Automatically added by bt-audio-server installer!" /etc/samba/smb.conf; then
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
cat btaudioserver.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/run_public.sh#" \
| sed -e "s#USER#$SUDO_USER#" > btaudioserver.service

systemctl enable $thisdir/btaudioserver.service
