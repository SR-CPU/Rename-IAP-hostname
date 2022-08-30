import json
import requests
import re
from time import sleep



def autologin(func):
    # @wraps(func)
    def inner(self, **kwargs):
        if self.logged_in is False:
            self.login()
            return func(self, **kwargs)
        else:
            return func(self, **kwargs)

    return inner


class InstantVC:
    def __init__(
        self,
        username,
        password,
        ip,
        port=4343,
        ssl_verify=False,
    ):

        self.username = username
        self.password = password
        self.port = port
        self.ip = ip
        self.logged_in = False
        self.sid = None
        self.session = requests.Session()
        self.baseurl = f"https://{ip}:{port}/rest"
        self.ssl_verify = ssl_verify
        self.headers = {"Content-Type": "application/json"}

    def login(self):

        url = f"{self.baseurl}/login"
        creds = {"user": self.username, "passwd": self.password}
        try:
            with requests.Session() as session:
                if not self.ssl_verify:
                    requests.packages.urllib3.disable_warnings()
                response = session.post(
                    url, json=creds, headers=self.headers, verify=self.ssl_verify
                )
                parsed = response.json()
                
                if parsed["Status"] == "Success":
                    self.logged_in = True
                    self.sid = parsed["sid"]
                    self.session = session
                    self.params = f"sid={self.sid}"
                return True
        except requests.exceptions.ConnectionError as e:
            return e

    def logout(self):
        """Log out of the VC"""
        url = f"{self.baseurl}/logout"
        data = json.dumps({})
        response = self.session.post(
            url,
            headers=self.headers,
            params=self.params,
            data=data,
            verify=self.ssl_verify,
        )
        parsed = response.json()
        if parsed["Status-code"] == "0":
            self.logged_in = False
            self.sid = ""
            self.session = None
            self.params = None



    @autologin
    def hostname(self, name="", iap_ip=""):

        url = f"{self.baseurl}/hostname"
        data = json.dumps({"iap_ip_addr": iap_ip, "hostname_info": {"hostname": name}})
        response = self.session.post(
            url,
            headers=self.headers,
            params=self.params,
            data=data,
            verify=self.ssl_verify,
        )
        if response.json().get("Status-code") == 0:
            return response.json()
