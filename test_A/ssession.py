import selenium.webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import urllib.request
from zipfile import ZipFile
import os
from pathlib import Path
import stat
import tarfile
import time
import json as js


def __assets(name, mode):
    top = __file__
    top = top[0:top.rfind("/")]
    return open(top + "/assets/" + name, mode)


def __asset_path() -> str:
    top = __file__
    top = top[0:top.rfind("/")]
    return top + "/assets/"


def __install_chrome_driver(args: list):
    if platform.system().lower() == "win32":
        add = "chromedriver_win32.zip"
    elif platform.system().lower() == "linux" or platform.system().lower() == "linux2":
        add = "chromedriver_linux64.zip"
    elif platform.system().lower() == "darwin":
        if platform.processor() == "M1":
            add = "chromedriver_mac64_m1.zip"
        else:
            add = "chromedriver_mac64.zip"
    else:
        raise BaseException("The Platform System: " + platform.system().lower() + " is not supported!")

    assets0 = __asset_path()

    return __load_chrome_driver_for_specific_version("95", assets0, add, args), "chromedriver"


"""
:returns driver.txt if found or null if not chrome
"""


def __load_chrome_driver_for_specific_version(version_google, assets0, add, args):
    chrome_driver_paths = {
        "95": "95.0.4638.17",
        "94": "94.0.4606.61",
        "93": "93.0.4577.63",
        "92": "92.0.4515.107",
        "91": "91.0.4472.101",
        "90": "90.0.4430.24",
        "89": "89.0.4389.23",
        "88": "88.0.4324.96",
        "87": "87.0.4280.88",
        "86": "86.0.4240.22",
        "85": "85.0.4183.87",
        "84": "84.0.4147.30",
        "83": "83.0.4103.39",
        "81": "81.0.4044.138",
        "80": "80.0.3987.106"
    }

    version_driver = chrome_driver_paths[version_google]

    chrome_driver_url = "https://chromedriver.storage.googleapis.com/" + version_driver + "/" + add
    urllib.request.urlretrieve(chrome_driver_url, assets0 + "chromedriver.zip")
    ZipFile(assets0 + "chromedriver.zip").extractall(assets0)
    os.remove(assets0 + "chromedriver.zip")

    f = Path(__asset_path() + "chromedriver")

    f.chmod(f.stat().st_mode | stat.S_IEXEC)

    try:

        options = selenium.webdriver.ChromeOptions()
        for arg in args:
            options.add_argument(arg)

        test_driver = selenium.webdriver.Chrome(options=options, executable_path=f.absolute())
        return test_driver
    except Exception as e:
        if isinstance(e, SessionNotCreatedException):
            h1 = "Current browser version is "
            version = e.msg[e.msg.index(h1) + len(h1):]
            version = version[0:2]
            return __load_chrome_driver_for_specific_version(version, assets0, add, args)
        else:
            if e.args is not None and len(e.args) > 0 and str(e.args[0]).startswith(
                    "unknown error: cannot find Google Chrome binary"):
                print("Chrome does not exist")
                return None
            return None


def __install_firefox_driver(args):
    version = "v0.30.0"
    arch = platform.architecture()[0:2]
    if platform.system().lower() == "win32":
        add = "geckodriver-" + version + "-win32.zip"
    elif platform.system().lower() == "win64":
        add = "geckodriver-" + version + "-win64.zip"
    elif platform.system().lower().startswith("linux"):
        add = "geckodriver-" + version + "-linux" + arch + ".tar.gz"
    elif platform.system().lower() == "darwin":
        if True:
            add = "geckodriver-" + version + "-macos.tar.gz"
        else:
            add = "geckodriver-" + version + "-macos-aarch64.tar.gz"
    else:
        raise BaseException("The Platform System: " + platform.system().lower() + " is not supported!")
    url = "https://github.com/mozilla/geckodriver/releases/download/" + version + "/" + add

    print(url)

    if add.endswith("gz"):
        out = "geckodriver.tar.gz"
    else:
        out = "geckodriver.zip"

    asset0 = __asset_path()

    urllib.request.urlretrieve(url, asset0 + out)

    if add.endswith("gz"):
        tar = tarfile.open(__asset_path() + out, "r:gz")
        tar.extractall(asset0)
        tar.close()
    else:
        ZipFile(asset0 + out).extractall(asset0)

    os.remove(asset0 + out)

    f = Path(__asset_path() + "geckodriver")

    f.chmod(f.stat().st_mode | stat.S_IEXEC)

    try:

        options = selenium.webdriver.FirefoxOptions()
        for arg in args:
            if arg == 'headless':
                options.headless = True
            options.add_argument(arg)

        test_driver = selenium.webdriver.Firefox(executable_path=f.absolute())
        return test_driver, "geckodriver"
    except Exception as e:
        if e.args is not None and len(e.args) > 0 and str(e.args[0]).startswith(
                "unknown error: cannot find Firefox binary"):
            print("Opera does not exist")
            return None
        return None, None


def __install_opera_driver(args: list):
    if platform.system().lower().startswith("win"):
        if platform.architecture()[0:2] == "32":
            add = "operadriver_win32.zip"
        else:
            add = "operadriver_win64.zip"
    elif platform.system().lower() == 'darwin':
        add = "operadriver_mac64.zip"
    elif platform.system().lower().startswith("linux"):
        add = "operadriver_linux64.zip"
    else:
        raise BaseException("The Platform System: " + platform.system().lower() + " is not supported!")

    assets0 = __asset_path()
    return __install_opera_driver_specific_version("80", add, assets0, args), "operadriver"


def __install_opera_driver_specific_version(opera_version, add, assets0, args):
    opera_driver_paths = {
        "80": "94.0.4606.61",
        "79": "93.0.4577.63",
        "78": "92.0.4515.107",
        "77": "91.0.4472.77",
        "76": "90.0.4430.85",
        "75": "89.0.4389.82",
        "74": "88.0.4324.104",
        "73": "87.0.4280.67",
        "72": "86.0.4240.80",
        "71": "85.0.4183.102",
        "70": "84.0.4147.89",
        "69": "83.0.4103.97",
        "68": "81.0.4044.113",
        "67": "80.0.3987.100",
        "66": "79.0.3945.79",
        "65": "78.0.3904.87",
        "64": "77.0.3865.120",
        "63": "76.0.3809.132",
        "62": "75.0.3770.100",
        "60": "2.45"
    }

    def __test_with_driver():
        f = Path(__asset_path() + "opera/operadriver")
        try:
            options = selenium.webdriver.ChromeOptions()
            for arg in args:
                options.add_argument(arg)
            test_driver = selenium.webdriver.Opera(options=options, executable_path=f.absolute())
            return test_driver
        except Exception as e:
            if isinstance(e, SessionNotCreatedException):
                h1 = "Current browser version is "
                version = e.msg[e.msg.index(h1) + len(h1):]
                version = version[0:2]
                return __install_opera_driver_specific_version(version, assets0, add)
            else:
                if e.args is not None and len(e.args) > 0 and str(e.args[0]).startswith(
                        "unknown error: cannot find Opera binary"):
                    print("Opera does not exist")
                    return None
                else:
                    return None

    f = Path(assets0 + "opera/")
    if f.exists():
        r = __test_with_driver()
        if r is not None:
            return r
        else:
            __remove_path(f)

    driver_version = opera_driver_paths[opera_version]

    chrome_driver_url = "https://github.com/operasoftware/operachromiumdriver/releases/download/v." + driver_version + "/" + add

    print(chrome_driver_url)

    urllib.request.urlretrieve(chrome_driver_url, assets0 + add)
    ZipFile(assets0 + add).extractall(assets0)
    os.rename(assets0 + add[0:add.rfind(".")], assets0 + "opera")
    os.remove(assets0 + add)

    f = Path(__asset_path() + "opera/operadriver")

    f.chmod(f.stat().st_mode | stat.S_IEXEC)

    return __test_with_driver()


def __remove_path(path: Path):
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        __remove_path(p)
    path.rmdir()


def __install_edge_driver(args):
    if platform.system().lower().startswith("win"):
        if platform.architecture()[0:2] == "32":
            add = "edgedriver_win32.zip"
        else:
            add = "edgedriver_win64.zip"
    elif platform.system().lower() == 'darwin':
        add = "edgedriver_mac64.zip"
    elif platform.system().lower().startswith("linux"):
        add = "edgedriver_linux64.zip"
    else:
        raise BaseException("The Platform System: " + platform.system().lower() + " is not supported!")

    return __install_edge_driver_specific_version("96", __asset_path(), add, args)


def __install_edge_driver_specific_version(version, asset0, add, args):
    edge_driver_paths = {
        "75": "75.0.139.20",
        "76": "76.0.183.0",
        "77": "77.0.237.0",
        "78": "78.0.277.0",
        "79": "79.0.313.0",
        "80": "80.0.361.9",
        "81": "81.0.416.77",
        "82": "82.0.459.1",
        "83": "83.0.478.64",
        "84": "84.0.524.0",
        "85": "85.0.564.8",
        "86": "86.0.622.69",
        "87": "87.0.669.0",  # up
        "88": "88.0.705.9",
        "89": "89.0.774.8",
        "90": "90.0.818.8",
        "91": "91.0.864.71",
        "92": "92.0.902.9",
        "93": "93.0.967.0",
        "94": "94.0.996.0",
        "95": "95.0.997.1",
        "96": "96.0.1044.0"
    }

    if int(version) < 88:
        if add.__contains__("linux"):
            add = str(add).replace("linux", "arm")

    # 88+ linux available

    driver_version = edge_driver_paths[version]

    url = "https://msedgedriver.azureedge.net/" + driver_version + "/" + add

    print(url)

    f = Path(__asset_path() + "msedgedriver")
    if f.exists():
        os.remove(f.absolute())

    urllib.request.urlretrieve(url, asset0 + add)
    ZipFile(asset0 + add).extractall(asset0)
    os.remove(asset0 + add)
    f = Path(__asset_path() + "msedgedriver")
    f.chmod(f.stat().st_mode | stat.S_IEXEC)

    try:
        options = selenium.webdriver.EdgeOptions()
        for arg in args:
            options.add_argument(arg)
        test_driver = selenium.webdriver.Edge(options=options, executable_path=f.absolute())
        return test_driver, "msedgedriver"
    except Exception as e:
        if isinstance(e, SessionNotCreatedException):
            h1 = "Current browser version is "
            version = e.msg[e.msg.index(h1) + len(h1):]
            version = version[0:2]
            return __install_edge_driver_specific_version(version, asset0, add)
        else:
            if e.args is not None and len(e.args) > 0 and str(e.args[0]).startswith(
                    "unknown error: cannot find Edge binary"):
                print("Edge does not exist")
                return None, None
            return None, None


def __install_safari_driver(args):
    try:
        if platform.system().lower() == "darwin":
            options = selenium.webdriver.ChromeOptions()
            for arg in args:
                options.add_argument(arg)
            return selenium.webdriver.Safari(options=options), "safari"
    except Exception as e:
        return None,None


def __install_driver(args: list):
    """d0, d1 = install_chrome_driver()
    if d0 is not None:
        return d0, d1"""
    '''return install_firefox_driver(), "geckodriver"'''
    if platform.system().lower() == "darwin":
        d0, d1 = __install_safari_driver(args)
        if d0 is not None:
            return d0, d1
    d0, d1 = __install_firefox_driver(args)
    if d0 is not None:
        return d0, d1
    d0, d1 = __install_chrome_driver(args)
    if d0 is not None:
        return d0, d1
    d0, d1 = __install_opera_driver(args)
    if d0 is not None:
        return d0, d1
    d0, d1 = __install_edge_driver(args)
    if d0 is not None:
        return d0, d1

    return None, None


"""elif data == "Ie":
                    return selenium.webdriver.Ie
                elif data == "WebKitGTK":
                    return selenium.webdriver.WebKitGTK
                elif data == "WPEWebKit":
                    return selenium.webdriver.WPEWebKit"""


def driver(args: list):
    """cannot get correct web browser via elumination"""
    if not Path(__asset_path() + "driver.txt").exists():
        __assets("driver.txt", "w").write("")
        data = None
    else:
        data = __assets("driver.txt", "r").read()
    if data is None or len(data) == 0:

        """installing drivers"""

        d0, name = __install_driver(args)

        if d0 is None:
            raise BaseException("Only Supporting Firefox, Safari, Google Chrome, Opera and Edge")

        __assets("driver.txt", "w").write(name)
        return d0

    else:
        if data == "chromedriver":
            try:
                options = selenium.webdriver.ChromeOptions()
                options.add_experimental_option('detach', True)
                for arg in args:
                    options.add_argument(arg)
                return selenium.webdriver.Chrome(options=options, executable_path=__asset_path() + "chromedriver")
            except Exception as e:
                if isinstance(e, selenium.common.exceptions.WebDriverException):
                    print("Browser went missing...")
                    __assets("driver.txt", "w").write("")
                    return driver(args)
        elif data == "geckodriver":
            try:
                options = selenium.webdriver.FirefoxOptions()
                for arg in args:
                    if arg == 'headless':
                        options.headless = True
                    options.add_argument(arg)
                return selenium.webdriver.Firefox(options=options, executable_path=__asset_path() + "geckodriver")
            except Exception as e:
                if isinstance(e, selenium.common.exceptions.WebDriverException):
                    print("Browser went missing...")
                    __assets("driver.txt", "w").write("")
                    return driver(args)
        elif data == "operadriver":
            try:
                options = selenium.webdriver.ChromeOptions()
                options.add_experimental_option('detach', True)
                for arg in args:
                    options.add_argument(arg)
                return selenium.webdriver.Opera(options=options, executable_path=__asset_path() + "opera/operadriver")
            except Exception as e:
                if isinstance(e, selenium.common.exceptions.WebDriverException):
                    print("Browser went missing...")
                    __assets("driver.txt", "w").write("")
                    return driver(args)
        elif data == "safari":
            try:
                options = selenium.webdriver.ChromeOptions()
                for arg in args:
                    options.add_argument(arg)
                return selenium.webdriver.Safari(options=options)
            except Exception as e:
                if isinstance(e, selenium.common.exceptions.WebDriverException):
                    print("Browser went missing...")
                    __assets("driver.txt", "w").write("")
                    return driver(args)
        elif data == "msedgedriver":
            try:
                options = selenium.webdriver.EdgeOptions()
                for arg in args:
                    options.add_argument(arg)
                return selenium.webdriver.Edge(options=options, executable_path=__asset_path() + "msedgedriver")
            except Exception as e:
                if isinstance(e, selenium.common.exceptions.WebDriverException):
                    print("Browser went missing...")
                    __assets("driver.txt", "w").write("")
                    return driver(args)
        else:
            __assets("driver.txt", "w").write("")
            return driver(args)


web_driver : selenium.webdriver.Ie = None


def get_credits() -> dict:
    s00 = open(__assets('password.json','r'))
    return js.loads(s00)

def close_web_driver():
    if web_driver is not None:
        web_driver.close()
        web_driver.quit()


def generate_cookie_id(credentials, force: bool = False) -> dict:

    global web_driver

    if not force:
        f = Path(__asset_path()+"cookie.json")
        if f.exists():
            f0 = open(f.absolute(), "r")
            # BUG #001 print(f0.read())
            print(f0.read())
            if len(f0.read()) > 0:
                return js.load(f0)

    args = [
        'headless',
        'window-size=1920x1080',
        "disable-gpu"
    ]

    web_driver = driver(args)

    web_driver.get("https://discovery.clarin.eu/?entityID=https%3A%2F%2Fweblicht.sfs.uni-tuebingen.de&return=https%3A"
                   "%2F%2Fweblicht.sfs.uni-tuebingen.de%2FShibboleth.sso%2FLogin%3FSAMLDS%3D1%26target%3Dss%253Amem"
                   "%253Ae1c684af520909460d9375a784812f01e3ae7434ce8f3c9268636708c98c364a")
    try:
        WebDriverWait(web_driver, 5).until(EC.presence_of_element_located((By.ID, "main")))
    finally:
        print("available")

        time.sleep(1)

        img_button = web_driver.find_element(By.XPATH,
                                             '//img[@src="https://www.clarin.eu/sites/default/files/clarin-logo.png"]')

        img_button.click()

        web_driver.implicitly_wait(3)

        # check if user arrived

        while not web_driver.current_url == "https://idm.clarin.eu/saml-idp/saml2idp-web-entry":
            print("waiting for web refresh")

        username_input = web_driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        password_input = web_driver.find_element(By.XPATH, "//input[@placeholder='Password']")

        web_driver.implicitly_wait(1)

        username_input.send_keys(credentials['username'])

        web_driver.implicitly_wait(1)

        password_input.send_keys(credentials['password'])

        click_element = web_driver.find_element(By.XPATH, "//div[@role='button']")

        web_driver.implicitly_wait(1)

        click_element.click()

        time.sleep(1)

        web_driver.get("https://weblicht.sfs.uni-tuebingen.de/rover/search")

        var = 0

        # load cookies
        while True:
            cookie = web_driver.get_cookie("_shibsession_64656661756c7468747470733a2f2f7765626c696368742e7366732e756e692d74756562696e67656e2e6465")
            if cookie is not None or var == 100000:
                break
            print(web_driver.get_cookies())
            var += 1
        if var != 100000:

            f0 = Path(__asset_path()+"cookie.json")
            f0.write_text("")
            file = open(f0.absolute(), "w")
            js.dump(cookie, file)

            return cookie
        else:
            return {}



