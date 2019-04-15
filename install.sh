pip install -r requirements.txt

path_param=$1

chmod a+x tft_projector.py
thisdir=`pwd`
cat tftprojector.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/tft_projector.py#" \
| sed -e "s#PATH#$path_param#" \
| sed -e "s#USER#$SUDO_USER#" > tftprojector.service

systemctl enable $thisdir/tftprojector.service
