#!/bin/bash

# Create systemd service for auto-start

cat <<EOF | sudo tee /etc/systemd/system/deep-research-bot.service
[Unit]
Description=Deep Research Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/deep-research-bot
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable deep-research-bot.service
echo "✅ Service created! Bot will auto-start on boot."
