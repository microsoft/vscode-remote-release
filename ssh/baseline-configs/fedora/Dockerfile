FROM fedora:latest

RUN dnf check-update || true && \
    dnf install -y openssh-server && \
    dnf clean all && \

    # Configuring ssh config
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/' /etc/ssh/sshd_config && \

    # Generating ssh keys
    ssh-keygen -A && \

    # Changing root password
    echo "root:foobar" | chpasswd

# TODO: expose only on an isolated docker network to avoid conflicts?
#       Think about how extension would communicate
EXPOSE 5671

CMD ["/usr/sbin/sshd", "-D", "-p", "5671"]
