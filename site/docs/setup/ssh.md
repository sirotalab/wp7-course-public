# SSH setup

This page will walk you through getting onto the HPC cluster from your laptop.

!!! warning "Draft"
    Pull the current content from the sirocampus shared clone before cohort start:

    - `/storage/share/sirocampus/docs/how-to/ssh/ssh-setup.md` — generating keys
    - `/storage/share/sirocampus/docs/how-to/ssh/ssh-config.md` — `~/.ssh/config` patterns
    - `/storage/share/sirocampus/docs/how-to/ssh/ssh-config-examples.md` — concrete examples
    - `/storage/share/sirocampus/docs/handbook/it/remote_access.md` — off-campus / VPN

## Your login account

The cohort shares 10 pooled accounts named `ephys01` through `ephys10`. Your
assigned account will be posted in `course-materials/README.md` before the
first session.

Multiple students may share the same `ephysNN` login. This means filesystem
ownership does **not** identify a student — see [HPC workspace](workspace.md)
for the per-student subdirectory convention.
