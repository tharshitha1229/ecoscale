#!/bin/bash
# ==============================================================================
# EcoScale AI - FCM360 / FCMCompute (OpenStack) Automated Setup Script
# Target OS: Ubuntu 22.04 / 24.04 LTS (Flavor: 2 vCPU, 4GB RAM, 10GB Disk)
# ==============================================================================

set -e

echo "🚀 [1/6] Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "📦 [2/6] Installing Docker, Python3, and core utilities..."
sudo apt install -y ca-certificates curl gnupg lsb-release git python3 python3-pip python3-venv

# Install Docker Engine if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker Engine..."
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

echo "👤 [3/6] Adding $USER to docker group (required for app.py Docker orchestration)..."
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock || true

echo "🐍 [4/6] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "🏗️ [5/6] Building backend Docker image (ecoscale-backend)..."
docker build -t ecoscale-backend ./backend
docker tag ecoscale-backend greencloud-backend 2>/dev/null || true

echo "⚙️ [6/6] Configuring persistent systemd service for Streamlit..."
APP_DIR=$(pwd)
CURRENT_USER=$USER

sudo bash -c "cat <<EOF > /etc/systemd/system/ecoscale.service
[Unit]
Description=EcoScale AI Streamlit Orchestrator
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=${CURRENT_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=5
Environment=PATH=${APP_DIR}/venv/bin:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable ecoscale.service
sudo systemctl restart ecoscale.service

echo ""
echo "=========================================================================="
echo "✅ EcoScale AI successfully deployed on FCMCompute!"
echo "🌐 View service status: sudo systemctl status ecoscale.service"
echo "📜 View live logs:      journalctl -u ecoscale.service -f"
echo "👉 Access your app at: http://$(curl -s ifconfig.me):8501"
echo "=========================================================================="
