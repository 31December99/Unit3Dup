Docker
######

You can run containers on both Windows and Linux

Linux
"""""
1) Install the Docker Engine and run the "Hello World!" test.
   https://docs.docker.com/engine/install/ubuntu/

2) Open the dockerfile and set your username inside the Dockerfile.

.. code-block:: ini

   The username must be the same on both the host and the container
   The owner must be the same on both the host and the container


3) Build the container

   cd in the \Unit3Dup\Docker folder and run:

    docker build -t unit3dup .

4) Run the bot using the unit3dup.sh script:

    chmod +x unit3du.sh

    ./unit3du.sh <-f> <-u> <-scan> <filepath>

Windows
"""""""

Install Desktop Docker

Like above except you need the unit3du.ps1 script
