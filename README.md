# Yoink

## Setup for Raspberrypi

1. Transfer repo to your pi. Either use git directly or send it from your local machine via ssh
```
scp -r yoink/ username@raspberrypi:/home/username/yoink
```
2. Install requirements globally. It is important to use sudo for the service to work.
```
sudo pip3 install -r requirements.txt
```
3. Create a .env file in the /yoink folder and store your telegram api key like this
```
API_KEY='your-api-key'
```

## Setup the service for the script

Now we're going to define the service to run the yoink script:

```
cd /lib/systemd/system/
sudo vi yoink.service
```
The service definition must be on the /lib/systemd/system folder. Be sure to switch 'username' for your name.

```
[Unit]
Description=yoink service
After=multi-user.target

[Service]
WorkingDirectory=/home/username/yoink
Type=simple
ExecStart=/usr/bin/python /home/username/yoink/src/backend/botservice.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Here we are creating a very simple service that runs the yoink script and if by any means is aborted is going to be restarted automatically. It also starts automatically when the pi restarts. You can check more on service's options in the next wiki: https://wiki.archlinux.org/index.php/systemd.

Now that we have our service we need to activate it:

```
sudo chmod 644 /lib/systemd/system/yoink.service
chmod +x /home/username/yoink.py
sudo systemctl daemon-reload
sudo systemctl enable yoink.service
sudo systemctl start yoink.service
```
### Service Tasks

For every change that we do on the /lib/systemd/system folder we need to execute a daemon-reload (third line of previous code). If we want to check the status of our service, you can execute:

```
sudo systemctl status yoink.service
```

In general:

#### Check status
```
sudo systemctl status yoink.service
```
#### Start service
```
sudo systemctl start yoink.service
```
#### Stop service
```
sudo systemctl stop yoink.service
```
#### Check service's log
```
sudo journalctl -f -u yoink.service
```
## Troubleshooting
+ When you use python version < 3.10 the kw_only flags of the dataclasses wont work. Either upgrade the python version or delete all kw_only flags. 

## References
+ https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f