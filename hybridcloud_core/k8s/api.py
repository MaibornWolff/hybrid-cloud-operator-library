import kubernetes
from .resources import Resource


def create_secret(namespace, name, data, labels={}, type="Opaque"):
    api = kubernetes.client.CoreV1Api()
    metadata = {
        "name": name,
        "namespace": namespace,
        "labels": labels,
    }
    body = kubernetes.client.V1Secret(metadata=metadata, string_data=data, type=type)
    api.create_namespaced_secret(namespace, body)


def get_secret(namespace, name):
    api = kubernetes.client.CoreV1Api()
    try:
        return api.read_namespaced_secret(name, namespace)
    except:
        return None


def update_secret(namespace, name, data, type="Opaque"):
    api = kubernetes.client.CoreV1Api()
    metadata = {
        "name": name,
        "namespace": namespace
    }
    body = kubernetes.client.V1Secret(metadata=metadata, string_data=data, type=type)
    api.patch_namespaced_secret(name, namespace, body)


def create_or_update_secret(namespace, name, data, labels={}, type="Opaque"):
    if get_secret(namespace, name):
        update_secret(namespace, name, data, type=type)
    else:
        create_secret(namespace, name, data, labels=labels, type=type)


def delete_secret(namespace, name):
    api = kubernetes.client.CoreV1Api()
    try:
        api.delete_namespaced_secret(name, namespace)
    except:
        pass


def patch_namespaced_custom_object(resource: Resource, namespace: str,  name: str, body):
    api = kubernetes.client.CustomObjectsApi()
    api.patch_namespaced_custom_object(resource.group, resource.version, namespace, resource.plural, name, body)


def get_namespaced_custom_object(resource: Resource, namespace: str, name: str):
    api = kubernetes.client.CustomObjectsApi()
    try:
        return api.get_namespaced_custom_object(resource.group, resource.version, namespace, resource.plural, name)
    except:
        return None


def patch_namespaced_custom_object_status(resource: Resource, namespace: str, name: str, status):
    body = {
        "metadata": {
            "name": name,
            "namespace": namespace
        },
        "status": status
    }
    patch_namespaced_custom_object(resource, namespace, name, body)


def delete_namespaced_custom_object(resource: Resource, namespace: str, name: str):
    api = kubernetes.client.CustomObjectsApi()
    try:
        api.delete_namespaced_custom_object(resource.group, resource.version, namespace, resource.plural, name)
    except:
        pass


def patch_cluster_custom_object(resource: Resource, name: str, body):
    api = kubernetes.client.CustomObjectsApi()
    api.patch_cluster_custom_object(resource.group, resource.version, resource.plural, name, body)


def get_cluster_custom_object(resource: Resource, name: str):
    api = kubernetes.client.CustomObjectsApi()
    try:
        return api.get_cluster_custom_object(resource.group, resource.version, resource.plural, name)
    except:
        return None


def patch_cluster_custom_object_status(resource: Resource, name: str, status):
    body = {
        "metadata": {
            "name": name
        },
        "status": status
    }
    patch_cluster_custom_object(resource, name, body)
