#!/bin/bash

eksctl utils write-kubeconfig --cluster=volga-test-cluster

helmfile --selector name=kuberay-operator sync --skip-deps

helmfile --selector name=ray-cluster sync --skip-deps

helmfile  --selector name=aws-load-balancer-controller sync --skip-deps

kubectl apply -f values/kuberay/ray-cluster/on-demand-service-external.yaml

kubectl apply -f values/kuberay/ray-cluster/on-demand-ingress.yaml

kubectl create ns locust

kubectl create cm volga-on-demand-locustfile -n locust --from-file values/deliveryhero/locust/volga_on_demand_locustfile.py

helmfile --selector name=locust sync --skip-deps