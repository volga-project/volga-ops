
FROM continuumio/miniconda3

RUN conda create -n env_py_3-10 python=3.10
RUN #echo "source activate env_py_3-10" > ~/.bashrc
ENV PATH /opt/conda/envs/env_py_3-10/bin:$PATH

RUN apt -y update
RUN apt -y install git
RUN apt -y install curl

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH /root/.cargo/bin:${PATH}

#RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

RUN git clone https://github.com/volga-project/volga.git
RUN cd /volga && conda run -n env_py_3-10 pip install .

RUN pip install maturin
RUN apt -y install build-essential
RUN conda install -n env_py_3-10 -c conda-forge gcc=12.1.0

RUN chown -R $(whoami) /volga/rust
RUN cd /volga/rust && conda run -n env_py_3-10 maturin develop

RUN conda run -n env_py_3-10 pip uninstall -y volga
ENV PYTHONPATH /volga:$PYTHONPATH

RUN conda run -n env_py_3-10 pip install ray[client]==2.34.0

COPY perf_test.py .

ENTRYPOINT conda run -n env_py_3-10 ray start --head && conda run -n env_py_3-10 python perf_test.py