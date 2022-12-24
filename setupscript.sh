#! /bin/sh.

sudo apt install ufw
sudo ufw allow openSSH
sudo ufw enable
sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
mkdir ~/myproject
cd ~/myproject
python3 -m venv myprojectenv
cp ~/cis3760-group-102/3760-102/a1.py ~/myproject
cp ~/cis3760-group-102/3760-102/search.py ~/myproject
cp -r ~/cis3760-group-102/3760-102/templates ~/myproject
cp -r ~/cis3760-group-102/3760-102/static ~/myproject
cp  parsed.xml ~/myproject
mv a1.py myproject.py
source myprojectenv/bin/activate
pip install wheel
pip install uwsgi flask
pip install lxml
sudo touch ~/myproject/wsgi.py
sudo echo -e "from myproject import app\n\nif __name__ == "__main__":\n\tapp.run()" | sudo tee ~/myproject/wsgi.py
deactivate
sudo touch ~/myproject/myproject.ini
sudo echo -e "[uwsgi]\nmodule = wsgi:app\n\nmaster = true\nprocesses = 5\n\nsocket = myproject.sock\n\nchmod-socket = 660\nvacuum = true\n\ndie-on-term = true" | sudo tee ~/myproject/myproject.ini
sudo touch /etc/systemd/system/myproject.service
sudo echo -e '[Unit]\nDescription=uWSGI instance to serve myproject\nAfter=network.target\n\n[Service]\nUser=ritchiedima\nGroup=www-data\nWorkingDirectory=/home/ritchiedima/myproject\nEnvironment="PATH=/home/ritchiedima/myproject/myprojectenv/bin"\nExecStart=/home/ritchiedima/myproject/myprojectenv/bin/uwsgi --ini myproject.ini\n\n[Install]\nWantedBy=multi-user.target' | sudo tee /etc/systemd/system/myproject.service
sudo systemctl start myproject
sudo systemctl enable myproject
sudo systemctl status myproject
sudo touch /etc/nginx/sites-available/myproject
sudo echo -e  "server {\n\tlisten 80;\n\tserver_name 34.130.204.52 www.34.130.204.52;\n\n\tlocation / {\n\t\tinclude uwsgi_params;\n\t\tuwsgi_pass unix:/home/sammy/myproject/myproject.sock;\n\t}\n}" | sudo tee /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo systemctl restart myproject
