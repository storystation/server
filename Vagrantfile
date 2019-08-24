# -*- mode: ruby -*-
# vi: set ft=ruby :

required_plugins = %w(vagrant-sshfs)

plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
if not plugins_to_install.empty?
  puts "Installing plugins: #{plugins_to_install.join(' ')}"
  if system "vagrant plugin install #{plugins_to_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort "Installation of one or more plugins has failed. Aborting."
  end
end

Vagrant.configure("2") do |config|
  config.vm.box = "generic/centos7"
  config.vm.network "private_network", ip: "192.168.33.109"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider "virtualbox" do |v|
    config.vm.synced_folder "./", "/home/vagrant/flask"
  end

  config.vm.provider "hyperv" do |v|
    config.vm.synced_folder "./", "/home/vagrant/flask", type: "sshfs", sshfs_opts_append: "-o umask=000,uid=1000,gid=1000,allow_other,follow_symlinks"
      # rsync__exclude: [ ".git/", ".vagrant/", "venv" ],
      # rsync__args: ["--verbose", "--archive", "-zu"]
  end

  config.vm.provider "docker" do |docker|
    config.vm.synced_folder "./", "/home/vagrant/flask"
    docker.image = "centos:7"
    docker.has_ssh = true
    docker.ports = [ "3333:3333" ]
  end

  config.vm.provision "shell", name: "Server setup script", inline: <<-SHELL
    echo "Provisioning the box, this will take a long time, be patient."
    echo "Installing packages..."
      yum list update > /dev/null 2>&1
      yum check-update > /dev/null 2>&1
      yum groupinstall -y "Development Tools" > /dev/null 2>&1
      yum install -y yum-utils sqlite-devel xz xz-devel \
        findutils bzip2 bzip2-devel expat-devel readline-devel \
        sqlite libffi-devel libcurl-devel gettext-devel openssl-devel \
        perl-CPAN perl-devel zlib-devel epel-release vim wget pwgen nginx> /dev/null 2>&1
    echo "Installing git..."
      wget https://quentinbouvier.fr/files/git_2.23.0_centos.tar.gz > /dev/null 2>&1
      tar zxf /home/vagrant/git_2.23.0_centos.tar.gz -C /usr/local/bin > /dev/null
      rm /home/vagrant/git_2.23.0_centos.tar.gz> /dev/null
    echo "Installing python..."
      sudo -u vagrant git clone https://github.com/pyenv/pyenv.git /home/vagrant/.pyenv > /dev/null 2>&1
      echo "export PATH=\\"\\$HOME/.pyenv/bin:\\$PATH\\"" >> /home/vagrant/.bashrc
      echo "eval \\"\\$(pyenv init -)\\"" >> /home/vagrant/.bashrc
      PYENV_PATH=/home/vagrant/.pyenv/bin
      $PYENV_PATH/pyenv init > /dev/null 2>&1
      wget https://quentinbouvier.fr/files/python_3.7.4_centos7.tar.gz > /dev/null 2>&1
      sudo -u vagrant mkdir /home/vagrant/.pyenv/versions/
      tar xfz python_3.7.4_centos7.tar.gz -C /home/vagrant/.pyenv/versions > /dev/null
      rm python_3.7.4_centos7.tar.gz > /dev/null
      chown -R vagrant:vagrant /home/vagrant/.pyenv/versions/
      chmod 755 /home/vagrant/.pyenv/versions/3.7.4
      sudo -u vagrant $PYENV_PATH/pyenv global 3.7.4
    echo "Installing docker..."
      (curl -fsSL https://get.docker.com/ | sudo -u vagrant sh) > /dev/null 2>&1
      systemctl start docker > /dev/null 2>&1
      systemctl enable docker > /dev/null 2>&1
      usermod -aG docker vagrant
      curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose > /dev/null 2>&1
      chmod +x /usr/local/bin/docker-compose
    echo "Create mongo DB container..."
      (cd /home/vagrant/flask && /usr/local/bin/docker-compose up -d) > /dev/null 2>&1
    echo "Installing services..."
      cp /home/vagrant/flask/utils/storystation-mongo.service /home/vagrant/flask/utils/storystation.service /etc/systemd/system
      sudo chown root:root /etc/systemd/system/storystation*
      sudo chmod 664 /etc/systemd/system/storystation*
      systemctl enable storystation.service
    echo "Configuring webserver"
      cp /home/vagrant/flask/utils/nginx.conf /etc/nginx/ -f
      systemctl enable nginx
      systemctl restart nginx
    echo "Starting webserver..."
      (cd /home/vagrant/flask && echo "$(pwd)" && ./setup.sh) > /dev/null 2>&1
      tries=0
      until [ "$(systemctl is-active storystation)" = "active" ] || [ $tries -gt 7 ]
      do
      ((tries=tries+1))
        echo "Trying to start server... ($tries)"
        systemctl start storystation
        sleep 2s
      done
      if [ $tries -gt 7 ]; then
        echo "Failed to start server. Try installing the dependencies manually and run 'systemctl start storystation'"
      else
        echo "Server successfully started. You can now browse http://$(ip a | grep -Po "192\.168\.[0-9]{1,3}\.[0-9]{1,3}" | head -1)"
      fi
      # TODO: find better iptables rule, this one sucks
      sudo iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited
  SHELL

  config.vm.provision "shell", run: 'always', name: "Adjust firewall rules", inline: <<-SHELL
    iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited
    semanage permissive -a httpd_t
    systemctl start storystation
  SHELL
end
