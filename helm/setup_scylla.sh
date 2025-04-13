#!/bin/bash

eksctl utils write-kubeconfig --cluster=volga-test-cluster

kubectl apply -f values/scylla/third-party/cert-manager.yaml

helmfile --selector name=scylla-operator sync --skip-deps

echo 'Waiting 60s for scylla-operator webhook to be ready...'
sleep 60

helmfile --selector name=scylla sync --skip-deps