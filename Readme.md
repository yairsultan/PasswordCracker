<!-- ABOUT THE PROJECT -->
## About The Project

Welcome to my Password Cracker!


<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Make sure docker daemon is running.
2. Clone the repo
   ```sh
   git clone https://github.com/yairsultan/PasswordCracker.git
   ```
3. Edit the docker-compose to run different amount of minion servers. (The default is one master and 8 minions)
4. Open ```\Master\app\hashes.txt``` and enter hashes to crack. (default hashes exist)
5. From the project directory start up the application by running
   ```sh
   docker-compose up
   ```
   Minion server depends on master server. (by using depends_on in the docker-compose)
   
   The minions will connect to the master on startup.
5. Go to http://localhost:8000/docs and swagger UI will open.

   To start cracking the phone number passwords, expand "/api/crack-hashes/" and click on "Try it out".

   Then, click "Execute" and the minion servers will start cracking the given hashes.



<!-- USAGE EXAMPLES -->
## Usage

Short screen recording to show how the password cracker works.


https://user-images.githubusercontent.com/75201013/201789298-76d44a88-8fd7-4ebc-90ab-fa919cb2bf18.mp4




