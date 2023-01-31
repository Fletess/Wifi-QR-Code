import qrcode
import getpass

from typing import Union

def wifi_code(ssid, hidden, auth_type, password: Union[str, None]):
    hidden = 'true' if hidden else 'false'

    if auth_type in ('WEP', 'WPA'):
        if not password:
            raise TypeError('Password required')
        return 'WIFI:T:{type};S:{ssid};P:{password};H:{hidden};;'.format(
            type=auth_type, ssid=ssid, password=password, hidden=hidden
        )
    elif auth_type == 'nopass':
        if password:
            raise TypeError('Password should be None')
        return 'WIFI:T:nopass;S:{ssid};H:{hidden};;'.format(
            ssid=ssid, hidden=hidden
        )

    raise ValueError('Unknown auth type')

def generate_code(ssid, hidden, auth_type, password: Union[str, None], **kwargs):
    return qrcode.make(wifi_code(ssid, hidden, auth_type, password), **kwargs).get_image()

def main():
    while True:
        ssid = input("SSID: ")
        if not ssid:
            print("Invalid SSID")

        hidden = input("Is the network hidden?").lower()
        if hidden in ['yes', 'y', 'true']:
            hidden = True
        elif hidden in ['', 'no', 'n', 'false']:
            hidden = False
        else:
            print("Invalid input")

        print("Authentication types: WPA/WPA2, WEP, nopass")
        authentication_type = input("Authentication type (default is "
                                    "WPA/WPA2): ").lower()
        if authentication_type in ['', 'wpa2', 'wpa', 'wpa/wpa2', 'wpa2/wpa']:
            authentication_type = 'WPA'
        elif authentication_type == 'WEP' or authentication_type == 'nopass':
            pass
        else:
            print("Input is not valid!")

        if authentication_type == 'nopass':
            password = None
            qrcode = generate_code(ssid, hidden, authentication_type, password)
            qrcode.save(ssid + '.png')
            print("The qr code has been stored in the current directory.")

            return

        password = input("Password: ")
        if password == "":
            print("Input not valid!")
        else:
            pass

        qrcode = generate_code(ssid, hidden, authentication_type, password)
        qrcode.save(ssid + '.png')
        print("The qr code has been stored in the current directory.")

if __name__ == "__main__":
    main()