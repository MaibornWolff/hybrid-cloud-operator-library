import kopf
from ..k8s import api 
from ..k8s.resources import Resource, Scope


ACTION_LABEL = "operator/action"


def ignore_control_label_change(diff):
    if diff:
        only_action_labels_removed = False
        for d in diff:
            d = repr(d)
            if "remove" in d and ACTION_LABEL in d:
                only_action_labels_removed = True
            else:
                only_action_labels_removed = False
        return only_action_labels_removed
    else:
        return False


def process_action_label(labels, commands, body, resource: Resource):
    found_control_labels = False
    for label, value in labels.items():
        if label == ACTION_LABEL:
            found_control_labels = True
            if value in commands:
                result = commands[value]()
                if result and isinstance(result, str):
                    kopf.event(body, type="operator", reason="action", message=result)
            else:
                kopf.event(body, type="operator", reason="failure", message=f"Unknown action: {value}")
    if found_control_labels:
        labels = dict(labels)
        labels[ACTION_LABEL] = None
        name = body["metadata"]["name"]
        patch = {
            "metadata": {
                "labels": labels
            }
        }
        if resource.scope == Scope.CLUSTER:
            api.patch_cluster_custom_object(resource, name, patch)
        else:
            namespace = body["metadata"]["namespace"]
            api.patch_namespaced_custom_object(resource, namespace, name, patch)


def has_label(labels, key, value=None):
    if key in labels:
        return value is None or labels[key] == value
    else:
        return False


def field_from_spec(spec, path, default=None, fail_if_missing=False):
    ptr = spec
    for var in path.split('.'):
        if ptr and var in ptr:
            ptr = ptr[var]
        else:
            if fail_if_missing:
                raise kopf.PermanentError(f"Missing spec field: {path}")
            return default
    return ptr
