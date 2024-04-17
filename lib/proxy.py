import os

from dotenv import load_dotenv

load_dotenv()

# создание экстеншна для прокси
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (os.getenv('PROXY_HOST'), os.getenv('PROXY_PORT'), os.getenv('PROXY_USERNAME'), os.getenv('PROXY_PASSWORD'))


def get_plugin_file():
    proxy_directory = 'extensions/ProxyAuthPlugin'
    if not os.path.isdir(proxy_directory):
        os.mkdir(proxy_directory)

    f = open("extensions/ProxyAuthPlugin/manifest.json", "w")
    f.write(manifest_json)
    f.close()

    f = open("extensions/ProxyAuthPlugin/background.js", "w")
    f.write(background_js)

    return proxy_directory
