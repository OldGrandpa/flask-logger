import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_token():
    if os.path.exists('token.json'):
        print("token.json already exists.")
        return

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json',
                                                     SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())

    print("token.json has been created.")


if __name__ == "__main__":
    get_token()
