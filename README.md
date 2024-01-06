# PorkCert

Simple script to fetch SSL certs from [Porkbun](https://porkbun.com/) domain registrar

## Description

[Porkbun](https://porkbun.com/) domain registrar automatically provides SSL certificates for domains. Unless you are web hosting through them, these will need to be downloaded every 3 months and updated on your serverThis

This repo includes:
* A python script to manually download the SSL cert bundle and store at desired location on server
* A shell script which builds above script as a Docker image and runs regularly as cron job to ensure that SSL certs are up to date

Certs are saved in traditional certbot names rather than default Porkbun names

### Running the python script to download and store certs once
```
git clone https://github.com/cjcon90/dotfiles.git && cd porkcert
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py -d {domain_name} -l {directory_to_save_certs}
```

### Setting cert renewal cron job
```
git clone https://github.com/cjcon90/dotfiles.git && cd porkcert
/install.sh
```
Answer prompts with domain name and directory to store certbundle

### API Keys

Either usage will prompt for API_KEY and API_SECRET_KEY from porkbun on first usage, and offer to store these in $HOME/.config/porkbun/keys.json

