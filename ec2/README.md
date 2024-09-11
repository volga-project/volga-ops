conda installation:
cd /tmp
curl https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh --output anaconda.sh
bash anaconda.sh
source ~/.bashrc
conda create --name env_py_3-10 python=3.10
conda activate env_py_3-10

rust installation:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

volga install:
pip install maturin
sudo git clone https://github.com/volga-project/volga.git

build rust:
sudo chown -R $(whoami) /volga/rust
sudo apt -y update && sudo apt -y install build-essential 

Run volga:
ray start --head
conda install -c conda-forge gcc=12.1.0
export PYTHONPATH=/volga:$PYTHONPATH
