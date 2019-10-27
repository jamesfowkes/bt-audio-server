## TFT module

## Samba

mkdir -p "/home/pi/cave-escape-pigeon-share"
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
cat pigeonspeaker.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/run_public.sh#" \
| sed -e "s#USER#$SUDO_USER#" > pigeonspeaker.service

systemctl enable $thisdir/pigeonspeaker.service
