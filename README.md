# pcs-container-update

Ansible module for uniform updates to pacemaker container resources.

# Requirements

1. The 'pcs' command-line interface utility
2. An HA cluster
3. Podman or Docker

# Example

Example playbook for including the module in your playbook

    - hosts: servers
      roles:
        - { role: jacksonsteiner.ansible_pcs_container_update }


Example playbook for using the module to update a container resource

    # Update the pacemaker resource postgres running in a podman container
    - name: Update Postgres
      pcs_container_update:
        name: postgres
    
    # Update the pacemaker resource nginx running in a podman container
    - name: Update nginx
      pcs_container_update:
        name: nginx
        engine: podman
    
    # Update the pacemaker resource nginx running in a docker container
    - name: Update nginx
      pcs_container_update:
        name: nginx
        engine: docker


# Documentation

Look at the full documentation and examples with

    ansible-doc -M library/ pcs_container_update
