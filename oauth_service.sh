#!/usr/bin/bash
installation_path="$2"
ip="$3"
fallback_ip=$(ip a | awk '/inet / && $2 !~ /^127\./ && $2 ~ /^192\.168\./ && $2 !~ /^10\./ {print $2; exit}')
ip=${ip:-$fallback_ip}
service_file="/etc/systemd/system/oauth.service"
echo $installation_path
cd $installation_path
chmod u+x ssl.sh
./ssl.sh $ip
if [[ ! -f "$service_file" ]]; then
  echo """
# https://github.com/vi0lin/oauth.git
[Unit]
Description=Oauth-Service
After=graphical-session.target
[Service]
Restart=always
Environment=DISPLAY=:0
RestartSec=3
User=user
ExecStart=bash -c \"cd $installation_path; python3 oauth.py --redirect_url $ip\"
ExecReload=echo Reloaded
Type=simple
[Install] 
WantedBy=default.target
WantedBy=multi-user.target
WantedBy=graphical-session.target
""" > $service_file
fi
systemctl enable oauth
systemctl start oauth
systemctl status oauth
