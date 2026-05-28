#!/bin/bash

# ==========================================
# Installs:
#   - AWS CLI
#   - Docker
# ==========================================

set -e

echo "=========================================="

# Detect OS
OS="$(uname -s)"

echo "Detected OS: $OS"


# ==========================================
# Function: Install AWS CLI
# ==========================================
install_aws_cli() {

    if command -v aws &> /dev/null
    then
        echo "AWS CLI already installed"
        aws --version
    else
        echo "Installing AWS CLI..."

        if [[ "$OS" == "Linux" ]]; then

            curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

            sudo yum install -y unzip || sudo apt-get install -y unzip

            unzip awscliv2.zip

            sudo ./aws/install

            rm -rf aws awscliv2.zip

        elif [[ "$OS" == "Darwin" ]]; then

            curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"

            sudo installer -pkg AWSCLIV2.pkg -target /

            rm AWSCLIV2.pkg

        else
            echo "Unsupported OS for AWS CLI installation"
            exit 1
        fi

        echo "AWS CLI installed successfully"
        aws --version
    fi
}

# ==========================================
# Function: Install Docker
# ==========================================
install_docker() {

    if command -v docker &> /dev/null
    then
        echo "Docker already installed"
        docker --version
    else
        echo "Installing Docker..."

        if [[ "$OS" == "Linux" ]]; then

            # Amazon Linux / RHEL / CentOS
            if command -v dnf &> /dev/null || command -v yum &> /dev/null; then

                sudo dnf -y update || sudo yum -y update
                sudo dnf -y install docker || sudo yum -y install docker

                sudo systemctl start docker
                sudo systemctl enable docker

                sudo usermod -aG docker $USER

            # Ubuntu / Debian
            elif command -v apt-get &> /dev/null; then

                sudo apt-get update

                sudo apt-get install -y \
                    ca-certificates \
                    curl \
                    gnupg \
                    lsb-release

                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
                    sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

                echo \
                  "deb [arch=$(dpkg --print-architecture) \
                  signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
                  https://download.docker.com/linux/ubuntu \
                  $(lsb_release -cs) stable" | \
                  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

                sudo apt-get update
                sudo apt-get install -y docker-ce docker-ce-cli containerd.io

                sudo systemctl start docker
                sudo systemctl enable docker

                sudo usermod -aG docker $USER

            else
                echo "Unsupported Linux distribution"
                exit 1
            fi

        elif [[ "$OS" == "Darwin" ]]; then
            echo "Please install Docker Desktop manually:"
            echo "https://www.docker.com/products/docker-desktop"
        fi

        echo "Docker installed successfully"
        docker --version

    fi

    # ==========================================
    # INSTALL DOCKER COMPOSE (IMPORTANT FIX)
    # ==========================================

    if command -v docker-compose &> /dev/null; then
        echo "docker-compose already installed"
        docker-compose --version
    else
        echo "Installing docker-compose (legacy, EC2 compatible)..."

        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
            -o /usr/local/bin/docker-compose

        sudo chmod +x /usr/local/bin/docker-compose

        echo "docker-compose installed successfully"
        docker-compose --version
    fi
}

# ==========================================
# Execute Installations
# ==========================================

# Install remaining tools
install_aws_cli
install_docker
echo ""
echo "=========================================="
echo " Setup Completed Successfully"
echo "=========================================="

echo ""
echo "IMPORTANT:"
echo "Logout and login again for Docker group changes to take effect."
echo ""

echo "Verify installations:"
echo "  aws --version"
echo "  docker --version"
echo "  python3 --version"
echo ""

echo "Docker installed successfully"
docker --version

# ==========================================
# Install Docker Compose (fallback method)
# ==========================================

if docker compose version &> /dev/null; then
    echo "Docker Compose (plugin) already available"
    docker compose version

elif command -v docker-compose &> /dev/null; then
    echo "Legacy docker-compose already installed"
    docker-compose --version

else
    echo "Installing Docker Compose manually..."

    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
        -o /usr/local/bin/docker-compose

    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose installed successfully"
    docker-compose --version
fi
