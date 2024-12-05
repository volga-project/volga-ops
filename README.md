# Running on Kubernetes

## Launching EKS cluster

Make sure you have a proper AWS account with right permissions. 
Install [eksctl](https://eksctl.io/)
Locate [cluster_config.yaml](https://github.com/volga-project/volga-ops/blob/master/eks/cluster_config.yaml) on your machine (cd into this dir)

Start Cluster
  - ```eksctl create cluster -f cluster_config.yaml```

Scale Cluster
  - ```eksctl scale nodegroup --cluster=volga-test-cluster --nodes=16 --name=ray-workers --nodes-min=0 --nodes-max=16```

Delete Cluster
  - ```eksctl delete cluster -f cluster_config.yaml --disable-nodegroup-eviction --force```

Note that the config uses hard-coded VPC configuration, you will need to create your own (or use default values given by eksctl)

## Launching Minikube cluster

Start Minikube cluster

- ```minikube config set memory 8192``` # sets memory per node
  
- ```minikube start --driver docker --nodes 5``` # cluster with 5 nodes

## Deploy

Deploy Ray cluster
- Intsall ```helmfile``` - https://github.com/helmfile/helmfile

- Make sure ```clusterType``` env val is set to ```minikube``` in ```helm/env_values.yaml```
- Install kuberay (from /helm folder):

  ```helmfile --selector name=kuberay-operator sync```
- Install Ray Cluster:

  ```helmfile --selector name=ray-cluster sync```
- To delete/recreate:

  ```helmfile --selector name=ray-cluster delete```,
  ```helmfile --selector name=ray-cluster sync```
- ```helm/values/kuberay/ray-cluster/values.yaml.gotmpl``` contains cluster configuration values (head/worker specs, ports, CPU/MEM reqs, etc.)

Make sure RayCluster's memory and CPU specs in helm values match whatever node you are using for your EKS cluster.

To run Volga tests (https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/test_remote_transfer.py as example)
- Build Python wheel with Rust binaries (from ```/volga/rust```), make sure you use python 3.10 (in your conda env as an example):


  ```docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build -i python3.10```

  This will create a ```.whl``` file in ```/volga/rust/target/wheels```, you will need to reference it in ```REMOTE_RAY_CLUSTER_TEST_RUNTIME_ENV``` python var in ```'py_modules'``` field in https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/testing_utils.py
  
- Forward 10001 port from ray head node (pod) so ray client can connect to it from local machine (to 12345 local port):

  ```kubectl port-forward svc/ray-cluster-kuberay-head-svc 12345:10001 -n ray-system```

- Run ```TestRemoteTransfer.test_n_to_n_parallel_on_ray(n=1, ray_addr=RAY_ADDR, runtime_env=REMOTE_RAY_CLUSTER_TEST_RUNTIME_ENV, multinode=True)```:

  ```python test_remote_transfer.py``` (from https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/)


# Running tests in Docker

```
cd docker
docker build . -t volga_perf
docker run volga_perf
```

Test script is in ```perf_test.py```. Everytime script is updated image needs to be re-built (```docker build . -t volga_perf```)
