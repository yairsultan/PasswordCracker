<!-- ABOUT THE PROJECT -->
## About The Project

Welcome to my Password Cracker!


<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Make sure docker daemon is running.
2. Edit the docker-compose to run diffrent amount of minion servers. (The default is one master and 8 minions)
3. Open \Master\app\hashes.txt and enter hashes to crack. (default hashes exist)
4. From the project directory start up the application by running
   ```sh
   docker-compose up
   ```
   Minion server depends on master server. (by using depends_on in the docker-compose)
   The minions will connect to the master on startup.
5. Go to http://localhost:8000/docs
   To start cracking the phone number passwords, expand "/api/crack-hashes/" and click on "Try it out".
   Then, click "Execute" and the minion servers will start cracking the given hashes.



<!-- USAGE EXAMPLES -->
## Usage

Short screen recording to show how the password cracker works.







