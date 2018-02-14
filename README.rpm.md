tendrl-cleanup
==============

Ansible roles and playbooks for cleanup of an existing tendrl setup
[Tendrl](http://tendrl.org/)!

Clone me:

```bash
git clone https://github.com/shtripat/tendrl-cleanup.git
```


## What does it do?

There are ansible roles for installation for cleaning up tendrl server and gluster nodes
which were setup earlier, based on 
[upstream documentation](https://github.com/Tendrl/documentation/wiki/Tendrl-Package-Installation-Reference):

* `tendrl-server`: cleanup of *Tendrl Server* machine (where api, web and
   etcd are running)
* `tendrl-storage-node`: cleanup of *Tendrl Storage Node* machine

See sample ansible playbook `site.yml.sample` to check how it fits together.

## Basic setup

Ansible Driven installation:

1) Install ansible >= 2.3
2) Get the code: `git clone https://github.com/shtripat/tendrl-cleanup.git`
3) Create Ansible inventory file with groups for `tendrl-server`
   and `gluster-servers`. Here is an example of inventory
   file for 4 node cluster with Gluster:

```
[gluster-servers]
gl1.example.com
gl2.example.com
gl3.example.com
gl4.example.com

[tendrl-server]
tendrl.example.com
```

4) Create `site.yml` file based on `site.yml.sample` and make sure to
   define all ansible variables there to suit.
5) Check that ssh can connect to all machines from the inventory file without
   asking for password or validation of public key by running:
   `$ ansible -i inventory_file -m ping all`.
   You should see ansible to show `"pong"` message for all machines.
   In case of any problems, you need to fix it
   before going on. If you are not sure what's wrong, consult documentation of
   ansible and/or ssh.
6) Run `$ ansible-playbook -i inventory_file site.yml`

## License

Distributed under the terms of the [GNU LGPL, version
2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) license,
tendrl-ansible is free and open source software.

