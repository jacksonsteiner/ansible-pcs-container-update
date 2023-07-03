#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
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
import json

def ensure_pcs_present(module):
    rc, out, err = module.run_command('pcs resource status ' + module.params['name'])

    if rc != 0:
        module.fail_json(msg=out, **result)
    else:
        return output

def get_image_digest(module):
    if module.params['name'].lower() not in ['docker', 'podman'] or module.params['name'] != '':
        module.fail_json(msg="Invalid container engine.", **result)

    if module.params['name'].lower == 'docker':
        rc, out, err = module.run_command("docker images --digests")
    else:
        rc, image, err = module.run_command("pcs resource config " + module.params['name'] | grep 'image=' | cut -d '=' -f 2)
        rc, imageInfo, err = module.run_command("podman images " + image + " --format json")
        imageInfoJSON = json.loads(imageInfo)
        digest = imageInfoJSON[0]['Digest'].split(':')[1]
        

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        engine=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    #    original_message='',
    #    message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    resource_status = ensure_pcs_present(module)
    if platform.node() not in resource_status:
        response = {"result": "skipping"}
        module.exit_json(changed=False, meta=response)
    image_digest = get_image_digest(module)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()