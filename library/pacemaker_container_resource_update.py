#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: pacemaker_contaniner_resource_update

short_description: Uniform update for pacemaker container resources

version_added: "0.0.1"

description: Longer description of pacemaker_container_resource_update

options:
    name:
        description: Name of the pacemaker container resource.
        required: true
        type: str
    engine:
        description: Container engine running containers. Can be Docker or Podman. Defaults to Podman.
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Jackson Steiner (@jacksonsteiner)
'''

EXAMPLES = r'''
# Update the pacemaker resource postgres running in a podman container
- name: Update Postgres
  my_namespace.my_collection.my_test:
    name: postgres

# Update the pacemaker resource nginx running in a podman container
- name: Update nginx
  my_namespace.my_collection.my_test:
    name: nginx
    engine: podman

# Update the pacemaker resource nginx running in a docker container
- name: Update nginx
  my_namespace.my_collection.my_test:
    name: nginx
    engine: docker
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import platform

def ensure_pcs_present(module, result):
    rc, out, err = module.run_command('pcs resource status ' + module.params['name'])
    if rc != 0:
        module.fail_json(msg=err, **result)
    else:
        return out

def get_pulled_image_digest(module, result):
    if module.params['engine'] != None and module.params['engine'].lower() not in ['docker', 'podman']:
        module.fail_json(msg='Invalid container engine.', **result)
    if module.params == None:
        engine = 'podman'
    else:
        engine = module.params['engine'].lower()
    rc, imageInfo, err = module.run_command(engine + ' images ' + module.params['name'] + ' --format "{{.Digest}}"')
    if rc != 0:
        module.fail_json(msg=err, **result)
    digest = imageInfo.split(':')[1]
    return digest, engine

def get_running_image_digest(module, result, engine):
    rc, imageInfo, err = module.run_command(engine + ' container inspect ' + module.params['name'] + ' --format "{{.ImageDigest}}"')
    if rc != 0:
        module.fail_json(msg=err, **result)
    digest = imageInfo.split(':')[1]
    return digest

def update_resource(module, result, pulledImageResource, runningImageResource):
    if pulledImageResource != runningImageResource:
        rc, out, err = module.run_command('pcs resource restart ' + module.params['name'])
        if rc != 0:
            module.fail_json(msg=err, **result)
        else:
            return True
    else:
        return False

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        engine=dict(type='str', required=False)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    resourceStatus = ensure_pcs_present(module, result)
    if platform.node() not in resourceStatus:
        response = {'result': 'skipping'}
        module.exit_json(changed=False, meta=response)
    pulledImageDigest, engine = get_pulled_image_digest(module, result)
    if pulledImageDigest == '':
        response = {'result': 'skipping'}
        module.exit_json(changed=False, meta=response)
    runningImageDigest = get_running_image_digest(module, result, engine)
    result['changed'] = update_resource(module, result, pulledImageDigest, runningImageDigest)
    if result['changed']:
        response = {'result': 'success'}
    else:
        response = {'result': 'ok'}
    module.exit_json(**result, meta=response)

def main():
    run_module()

if __name__ == '__main__':
    main()