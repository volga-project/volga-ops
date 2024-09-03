#!/bin/bash
TEMPLATE_PATH="template.yaml"
KOPS_CLUSTER_CONFIG_PATH="cluster_config.yaml"
VALUES_PATH="values.yaml"
CLUSTER_NAME=$(yq '.cluster_name' $VALUES_PATH)
STATE="s3://$(yq '.kops_s3_bucket_name' $VALUES_PATH)"

echo "Cluster ${CLUSTER_NAME}, state ${STATE}"

kops delete cluster --state $STATE --name $CLUSTER_NAME --yes
echo "Cleared old state at "$STATE

kops toolbox template --name ${CLUSTER_NAME} --values ${VALUES_PATH} --template ${TEMPLATE_PATH} --format-yaml > ${KOPS_CLUSTER_CONFIG_PATH}
echo "Kops cluster config in ${KOPS_CLUSTER_CONFIG_PATH}"

kops create -f ${KOPS_CLUSTER_CONFIG_PATH} --name $CLUSTER_NAME --state $STATE
echo "Created cluster "$CLUSTER_NAME

echo "Deploying resources"
kops update cluster --name $CLUSTER_NAME --state $STATE --yes
echo "Deployed resources"

kops create secret --name $CLUSTER_NAME --state $STATE sshpublickey admin -i ~/.ssh/id_rsa.pub
echo "Created secret sshpublickey"

kops export kubeconfig --admin --name $CLUSTER_NAME --state $STATE
echo "Done"