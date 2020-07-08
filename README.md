Country Chain Bot is a telegram bot which implements the «country chain» game

## How to run the bot
1. [Create](https://core.telegram.org/bots#creating-a-new-bot) a telegram bot
2. [Install](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community) docker
3. [Install](https://docs.docker.com/compose/install) docker compose
4. Clone the repository
```bash
git clone https://github.com/duketemon/country-chain.git
```
5. Put your telegram bot token to the [docker-compose](https://github.com/duketemon/country-chain/blob/master/docker-compose.yml) file
6. Run the following command
```bash
sudo docker-compose up -d
```
7. Play using a Telegram client

## How to deploy the bot
As a deployment environment you can use a local host, [GCP Compute Engine](https://cloud.google.com/compute), [Amazon EC2](https://aws.amazon.com/ec2) or anything else
