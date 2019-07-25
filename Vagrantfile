# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "private_network", ip: "192.168.33.109"
  config.vm.synced_folder "./", "/var/www/html"

  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install python3.7 python3.7-venv python3-venv python3-pip mongodb libapache2-mod-python apache2 -y
    sudo a2dismod mpm_event #> désactivons les processus multithreading.
    sudo a2enmod mpm_prefork cgi #> permission explicite d’exécuter des scripts
    sudo a2enmod alias
    sudo a2enmod cgi
    sudo sed -i 4i"<Directory /var/www/html>" /etc/apache2/sites-enabled/000-default.conf
    sudo sed -i 5i"Options +ExecCGI" /etc/apache2/sites-enabled/000-default.conf
    sudo sed -i 6i"DirectoryIndex index.py" /etc/apache2/sites-enabled/000-default.conf
    sudo sed -i 7i"AllowOverride All" /etc/apache2/sites-enabled/000-default.conf
    sudo sed -i 8i"AddHandler cgi-script .py" /etc/apache2/sites-enabled/000-default.conf
    sudo sed -i 9i"</Directory>" /etc/apache2/sites-enabled/000-default.conf
    sudo service apache2 restart
    # echo "Création du fichier index.py"
    # cd /var/www/html
    # sudo touch index.py
    # sudo sed -i 1i"#!/usr/bin/env python" index.py
    # sudo sed -i 2i"import cgi" index.py
    # sudo sed -i 3i"import cgitb" index.py
    # sudo sed -i 4i"cgitb.enable()" index.py
    # sudo sed -i 6i"print('Content-Type: text/html')" index.py
    # sudo sed -i 7i"print('<b>Hello python</b>')" index.py
    # echo "Donne les droits au fichier"
    # sudo chmod 755 index.py
    # echo "Fin D'Installation !!"
    sudo systemctl enable mongodb
    cd ~/flask
    ./setup.sh
  SHELL
end
