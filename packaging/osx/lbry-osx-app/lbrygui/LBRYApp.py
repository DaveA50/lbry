import AppKit
import webbrowser
import sys
import os
import logging
import socket
import platform
import shutil
from appdirs import user_data_dir

from PyObjCTools import AppHelper

from twisted.internet import reactor
from twisted.web import server

import Foundation
bundle = Foundation.NSBundle.mainBundle()
lbrycrdd_path = bundle.pathForResource_ofType_('lbrycrdd', None)
lbrycrdd_path_conf = os.path.join(os.path.expanduser("~"), ".lbrycrddpath.conf")
wallet_dir = user_data_dir("lbrycrd")

if not os.path.isdir(wallet_dir):
    shutil.os.mkdir(wallet_dir)

if not os.path.isfile(lbrycrdd_path_conf):
    f = open(lbrycrdd_path_conf, "w")
    f.write(lbrycrdd_path)
    f.close()

from lbrynet.lbrynet_daemon.DaemonServer import DaemonServer, DaemonRequest
from lbrynet.conf import API_PORT, API_INTERFACE, ICON_PATH, APP_NAME
from lbrynet.conf import UI_ADDRESS

if platform.mac_ver()[0] >= "10.10":
    from LBRYNotify import LBRYNotify

log = logging.getLogger(__name__)

REMOTE_SERVER = "www.google.com"


def test_internet_connection():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        return False


class LBRYDaemonApp(AppKit.NSApplication):
    def finishLaunching(self):
        self.connection = False
        statusbar = AppKit.NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(AppKit.NSVariableStatusItemLength)
        self.icon = AppKit.NSImage.alloc().initByReferencingFile_(ICON_PATH)
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)
        self.menubarMenu = AppKit.NSMenu.alloc().init()
        self.open = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Open", "openui:", "")
        self.menubarMenu.addItem_(self.open)
        self.quit = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "replyToApplicationShouldTerminate:", "")
        self.menubarMenu.addItem_(self.quit)
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_(APP_NAME)


        if test_internet_connection():
            if platform.mac_ver()[0] >= "10.10":
                LBRYNotify("Starting LBRY")
        else:
            if platform.mac_ver()[0] >= "10.10":
                LBRYNotify("LBRY needs an internet connection to start, try again when one is available")
            sys.exit(0)


        lbry = DaemonServer()
        d = lbry.start()
        d.addCallback(lambda _: webbrowser.open(UI_ADDRESS))
        lbrynet_server = server.Site(lbry.root)
        lbrynet_server.requestFactory = DaemonRequest
        reactor.listenTCP(API_PORT, lbrynet_server, interface=API_INTERFACE)

    def openui_(self, sender):
        webbrowser.open(UI_ADDRESS)

    def replyToApplicationShouldTerminate_(self, shouldTerminate):
        if platform.mac_ver()[0] >= "10.10":
            LBRYNotify("Goodbye!")
        reactor.stop()
