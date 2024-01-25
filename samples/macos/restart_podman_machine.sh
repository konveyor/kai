#!/bin/sh

# Default variables can be overriden from environment
: ${VM_NAME="kantra"}
: ${MEM=8192}
: ${CPUS=4}
: ${DISK_SIZE=100}

# See https://github.com/konveyor/kantra/issues/91
# See https://github.com/containers/podman/issues/16106#issuecomment-1317188581
# Setting file limits to unlimited on the Mac Host
ulimit -n unlimited
podman machine stop $VM_NAME
podman machine rm $VM_NAME -f
podman machine init $VM_NAME -v $HOME:$HOME -v /private/tmp:/private/tmp -v /var/folders/:/var/folders/
podman machine set $VM_NAME --cpus $CPUS --memory $MEM --disk-size $DISK_SIZE
podman system connection default $VM_NAME
podman machine start $VM_NAME
# Workaround for setting file limits inside of the podman machine VM
# https://github.com/konveyor/kantra/issues/111
podman machine ssh kantra "echo *      soft      nofile      65535 | sudo tee -a /etc/security/limits.conf"
podman machine ssh kantra "echo *      hard      nofile      65535 | sudo tee -a /etc/security/limits.conf"
podman machine ssh kantra ulimit -n #To confirm the change has taken effect
