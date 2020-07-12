# Installation

```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install osrsbox
apt install mitmproxy
```

# Windows Environment Variable

```
JAVA_TOOL_OPTIONS=-Drunelite.http-service.url="http://localhost:8080"
```

# Running

```bash
mitmdump -s mitm.py --mode reverse:http://api.runelite.net --listen-host 0.0.0.0
```
