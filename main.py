import requests
import json
import click
import typing as t
from pathlib import Path
import sys

API_KEY: str = "API_KEY"
SECRET_KEY: str = "SECRET_API_KEY"
KEY_NAMES = [API_KEY, SECRET_KEY]
CONFIG_DIR: str = f"{Path.home()}/.config/porkcert"
KEYFILE = f"{CONFIG_DIR}/keys.json"
SSL_ENDPOINT = "https://porkbun.com/api/json/v3/ssl/retrieve/{}"

# Keep names in line with standard certbot names
CERT_NAME_TO_FILE = {
    "certificatechain": "fullchain.pem",
    "intermediatecertificate": "chain.pem",
    "privatekey": "privkey.pem",
    "publickey": "cert.pem",
}


def get_keys():
    """
    Check if keys exist at .config/porkcert/keys.json and fetch if so
    Otherwise prompt user to input and save
    """
    if Path(KEYFILE).exists():
        with open(KEYFILE, "r") as f:
            data = json.loads(f.read())
        if all(data.get(key, None) for key in KEY_NAMES):
            click.echo(f"Loaded API keys from {KEYFILE}")
            return data[API_KEY], data[SECRET_KEY]

    keys: t.Dict[str, str] = {}
    for key_type in KEY_NAMES:
        value = click.prompt(f"Enter value for {key_type}", hide_input=True)
        keys[key_type] = value

    if click.confirm(
        "Do you want to store these keys to "
        f"{KEYFILE.replace(f'{Path.home()}/', '$HOME/')}?",
        default=True,
    ):
        Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
        with open(KEYFILE, "w") as f:
            json.dump(keys, f, indent=2)
    exit(0)

    return keys[API_KEY], keys[SECRET_KEY]


def request_certs(domain: str, apikey: str, secretkey: str) -> t.Dict[str, str]:
    """
    Get JSON reponse from porkcert API
    """
    js_keys = {"apikey": apikey, "secretapikey": secretkey}
    response = requests.post(SSL_ENDPOINT.format(domain), json=js_keys).text
    return json.loads(response)


@click.command()
@click.option(
    "--domain",
    "-d",
    help="Domain we are requesting the SSL certs in relation to",
    required=True,
)
@click.option(
    "--location",
    "-l",
    help="Directory to store the downloaded SSL certs",
    required=True,
)
def main(domain: str = "", location: str = "") -> None:
    apikey, secretkey = get_keys()
    certs = request_certs(domain, apikey, secretkey)
    if certs["status"] == "ERROR":
        click.secho(f"ERROR - {certs['message']}", fg="red")
        sys.exit(1)
    Path(location).mkdir(parents=True, exist_ok=True)
    for cert_name, file_name in CERT_NAME_TO_FILE.items():
        cert = certs[cert_name]
        path = str(Path(location)) + "/" + file_name
        with open(path, "w") as f:
            f.write(cert)


if __name__ == "__main__":
    main()
