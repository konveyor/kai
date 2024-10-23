#!/bin/sh

full_version=$(podman -v | awk '{print $3}')
podman_major_version=$(echo "${full_version}" | cut -d '.' -f1)

# Default variables can be overriden from environment
: ${VM_NAME="kantra"}
: ${MEM=8192}
: ${CPUS=4}
# Podman 5 will NOT run with '100' GB, it tells us it needs more than 100GB
# "Error: new disk size must be larger than 100 GB"
: ${DISK_SIZE=101}

# See https://github.com/konveyor/kantra/issues/91
# See https://github.com/containers/podman/issues/16106#issuecomment-1317188581
# Setting file limits to unlimited on the Mac Host
ulimit -n unlimited
podman machine stop "${VM_NAME}"
podman machine rm "${VM_NAME}" -f

if [ "${podman_major_version}" -eq 4 ]; then
	podman machine init "${VM_NAME}" -v "${HOME}":"${HOME}" -v /private/tmp:/private/tmp -v /var/folders/:/var/folders/
else
	# for podman 5.x we do not want to add the volume mounts, they are included by default and if we specify them we have odd behavior
	podman machine init "${VM_NAME}"
fi

if ! podman machine set "${VM_NAME}" --cpus "${CPUS}" --memory "${MEM}" --disk-size "${DISK_SIZE}"; then
	# We've had several subtle issues of not being able to set the memory and analysis later locking up
	# So adding an explicit error check
	exit 1
fi

podman system connection default "${VM_NAME}"
podman machine start "${VM_NAME}"
# Workaround for setting file limits inside of the podman machine VM
# https://github.com/konveyor/kantra/issues/111
podman machine ssh kantra "echo *      soft      nofile      65535 | sudo tee -a /etc/security/limits.conf"
podman machine ssh kantra "echo *      hard      nofile      65535 | sudo tee -a /etc/security/limits.conf"
podman machine ssh kantra ulimit -n #To confirm the change has taken effect
