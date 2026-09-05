FROM fedora:latest

RUN dnf check-update || true && \
    dnf install -y openssh-server wget && \
    dnf clean all && \

    # Configuring ssh config
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/' /etc/ssh/sshd_config && \

    # Generating ssh keys
    ssh-keygen -A && \

    # Changing root password
    echo "root:foobar" | chpasswd

EXPOSE 5670

CMD ["/usr/sbin/sshd", "-D", "-p", "5670"]
