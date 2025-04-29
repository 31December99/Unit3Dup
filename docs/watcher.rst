
Always use **python start.py** when you want to send a command to the bot

- Open the black console window and navigate to the bot folder
- The bot can accept one or more commands (**flags**).Depending on what you want to do


Flag watcher
********************

`-watcher` it reads the contents of a folder and moves them to another destination folder, then uploads everything to the tracker

How to use watcher
==============================

The flag does not accept parameters

.. code-block:: python

    python start.py -watcher

The default folders are:

watcher_path

watcher_destination_path

How to configure the watcher
==============================

Open the `Unit3D.json` file with a text editor and set the attribute:

WATCHER_INTERVAL

Every WATCHER_INTERVAL (seconds), it checks `watcher_path`, then moves everything to `watcher_destination_path`, and uploads it to the tracker


How to create a service with the watcher
========================================
    sudo nano /etc/systemd/system/unit3dupbot.service

.. code-block:: ini

    [Unit]
    Description=Unit3D bot uploader
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory=/home/parzival/Unit3Dup
    ExecStart=/usr/bin/python3 /home/parzival/Unit3Dup/start.py -watcher
    StandardOutput=file:/home/parzival/unit3dbot.log
    StandardError=file:/home/parzival/unit3dbot_error.log
    User=parzival

    [Install]
    WantedBy=multi-user.target

.. code-block:: python

    Reload the demon
    Restart and check the status

.. code-block:: ini

    parzival@parivalsrv:~/Unit3Dup$ sudo systemctl daemon-reload
    parzival@parivalsrv:~/Unit3Dup$ sudo systemctl enable unit3dupbot.service
    parzival@parivalsrv:~/Unit3Dup$ sudo systemctl restart unit3dupbot.service
    parzival@parivalsrv:~/Unit3Dup$ sudo systemctl status unit3dupbot.service
    ● unit3dupbot.service - Unit3D bot uploader
         Loaded: loaded (/etc/systemd/system/unit3dupbot.service; enabled; vendor preset: enabled)
         Active: active (running) since Mon 2025-04-28 15:34:29 UTC; 4s ago
       Main PID: 3093 (python3)
          Tasks: 1 (limit: 9350)
         Memory: 46.6M
            CPU: 420ms
         CGroup: /system.slice/unit3dupbot.service
                 └─3093 /usr/bin/python3 /home/parzival/Unit3Dup/start.py -watcher


