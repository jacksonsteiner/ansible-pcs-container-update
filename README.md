# pcs-container-update

Ansible module for uniform updates to pacemaker container resources.

# Requirements

1. The 'pcs' command-line interface utility
2. A Pacemaker High-Availability cluster with container resources
3. Podman or Docker

# Full Overview
This is a module for updating container resources being managed by pacemaker in a high-availability cluster. It finds the node the resources are running on, then compares digests of the pulled image and the running container image, and updates the container with the new image if the digests are different. This role uses the 'pcs' command-line interface tool to restart the resource if the digests are not equal. It is required to first pull newer images using Podman/Docker modules with Ansible. This module does not do that for you. It also does not provide rolling updates; this is a uniform update, meaning the resource will experience downtime while it restarts with the newer image. If the resource has dependenies, such as in a resource group, the dependent resources will be stopped to update the given container resource.

# Example

Example playbook for including the module in your playbook

    - hosts: servers
      roles:
        - jacksonsteiner.ansible_pcs_container_update


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
