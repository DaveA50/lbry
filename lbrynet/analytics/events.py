import logging

from lbrynet.analytics import utils


log = logging.getLogger(__name__)


def get_sd_hash(stream_info):
    if not stream_info:
        return None
    try:
        return stream_info['sources']['lbry_sd_hash']
    except (KeyError, TypeError, ValueError):
        log.debug('Failed to get sd_hash from %s', stream_info, exc_info=True)
        return None


class Events(object):
    def __init__(self, context, lbry_id, session_id):
        self.context = context
        self.lbry_id = lbry_id
        self.session_id = session_id

    def heartbeat(self):
        return {
            'userId': 'lbry',
            'event': 'Heartbeat',
            'properties': {
                'lbry_id': self.lbry_id,
                'session_id': self.session_id
            },
            'context': self.context,
            'timestamp': utils.now()
        }

    def download_started(self, name, stream_info=None):
        return {
            'userId': 'lbry',
            'event': 'Download Started',
            'properties': {
                'lbry_id': self.lbry_id,
                'session_id': self.session_id,
                'name': name,
                'stream_info': get_sd_hash(stream_info)
            },
            'context': self.context,
            'timestamp': utils.now()
        }


def make_context(platform, wallet, is_dev=False):
    # TODO: distinguish between developer and release instances
    return {
        'is_dev': is_dev,
        'app': {
            'name': 'lbrynet',
            'version': platform['lbrynet_version'],
            'ui_version': platform['ui_version'],
            'python_version': platform['python_version'],
            'wallet': {
                'name': wallet,
                # TODO: add in version info for lbrycrdd
                'version': platform['lbryum_version'] if wallet == 'lbryum' else None
            },
        },
        # TODO: expand os info to give linux/osx specific info
        'os': {
            'name': platform['os_system'],
            'version': platform['os_release']
        },
        'library': {
            'name': 'lbrynet-analytics',
            'version': '1.0.0'
        },
    }
