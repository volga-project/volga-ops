Deploying Ray cluster
- Intsall ```helmfile``` - https://github.com/helmfile/helmfile 
- Install kuberay (from /helm folder):

  ```helmfile --selector name=kuberay-operator sync```
- Install Ray Cluster:

  ```helmfile --selector name=ray-cluster sync```
- To delete/recreate:

  ```helmfile --selector name=ray-cluster delete```,
  ```helmfile --selector name=ray-cluster sync```
- ```helm/values/kuberay/ray-cluster/values.yaml.gotmpl``` contains cluster configuration values (head/worker specs, ports, CPU/MEM reqs, etc.)

To run Volga tests (https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/test_remote_transfer.py as example)
- Build Python wheel with Rust binaries (from ```/volga/rust```), make sure you use python 3.10 (in your conda env as an example):


  ```docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build -i python3.10```

  This will create a ```.whl``` file in ```/volga/rust/target/wheels```, you will need to reference it in ```REMOTE_RAY_CLUSTER_TEST_RUNTIME_ENV``` python var in https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/testing_utils.py
  
- Forward 10001 port from ray head node (pod) so ray client can connect to it from local machine (to 12345 local port):

  ```kubectl port-forward svc/ray-cluster-kuberay-head-svc 12345:10001 -n ray-system```

- Run ```TestRemoteTransfer.test_n_to_n_parallel_on_ray(n=1, ray_addr=RAY_ADDR, runtime_env=REMOTE_RAY_CLUSTER_TEST_RUNTIME_ENV, multinode=True)```:

  ```python test_remote_transfer.py``` (from https://github.com/volga-project/volga/blob/master/volga/streaming/runtime/network/)
