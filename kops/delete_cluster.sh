#!/bin/bash
VALUES_PATH="values.yaml"
CLUSTER_NAME=$(yq '.cluster_name' $VALUES_PATH)
STATE="s3://$(yq '.kops_s3_bucket_name' $VALUES_PATH)"

kops delete cluster --yes --name $CLUSTER_NAME --state $STATE

echo "Cluster deletion done"