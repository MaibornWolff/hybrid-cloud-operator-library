import base64
from kubernetes.client.models.v1_secret import V1Secret


def decode_secret_data(secret: V1Secret):
    result = dict()
    if not secret.data:
        return result
    for key, data in secret.data.items():
        result[key] = base64.b64decode(data).decode("utf-8")
    return result
