# path to local prom service discovery file /tmp/ray/prom_metrics_service_discovery.json
import atexit
import subprocess

import kubernetes
from kubernetes import client
CLUSTER = 'minikube-1'
WORKER_GROUP_NAME = 'test-group'
NAMESPACE = 'ray-system'


kubernetes.config.load_kube_config(context=CLUSTER)
core_api = kubernetes.client.CoreV1Api()

created_services_names = []
pods = core_api.list_namespaced_pod(namespace=NAMESPACE, label_selector=f'ray.io/group={WORKER_GROUP_NAME}')
for pod in pods.items:
    pod_name = pod.metadata.name
    service_name = f'{pod_name}-svc'

    core_api.patch_namespaced_pod(pod_name, NAMESPACE, {'metadata':{'labels':{'name':pod_name}}})
    body = client.V1Service(
        api_version='v1',
        kind='Service',
        metadata=client.V1ObjectMeta(
            name=service_name,
            labels={'kubefwd': 'true'}
        ),

        spec=client.V1ServiceSpec(
            selector={'name': pod_name},
            type='ClusterIP',
            ports=[client.V1ServicePort(
                port=8080,
                target_port=8080
            )]
        )
    )
    try:
        core_api.create_namespaced_service(namespace=NAMESPACE, body=body)
    except kubernetes.client.exceptions.ApiException as e:
        if e.reason == 'Conflict':
            print(f'{service_name} already exists')

    created_services_names.append(service_name)
print(f'Created {len(created_services_names)} services')


def delete_services():
    for service_name in created_services_names:
        core_api.delete_namespaced_service(name=service_name, namespace=NAMESPACE)
    print(f'Deleted {len(created_services_names)} services')

atexit.register(delete_services)

process = subprocess.Popen(f'kubefwd svc -n {NAMESPACE} -l kubefwd=true', shell=True)
process.wait()