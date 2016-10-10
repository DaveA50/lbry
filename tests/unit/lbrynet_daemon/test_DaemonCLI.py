from twisted.trial import unittest
from lbrynet.lbrynet_daemon import DaemonCLI


class DaemonCLITests(unittest.TestCase):
    def test_guess_type(self):
        self.assertEqual('0.3.8', DaemonCLI.guess_type('0.3.8'))
        self.assertEqual(0.3, DaemonCLI.guess_type('0.3'))
        self.assertEqual(3, DaemonCLI.guess_type('3'))
        self.assertEqual('VdNmakxFORPSyfCprAD/eDDPk5TY9QYtSA==', DaemonCLI.guess_type('VdNmakxFORPSyfCprAD/eDDPk5TY9QYtSA=='))
        self.assertEqual(0.3, DaemonCLI.guess_type('0.3'))

    def test_get_params(self):
        test_params = [
            'b64address=VdNmakxFORPSyfCprAD/eDDPk5TY9QYtSA==',
            'name=test',
            'amount=5.3',
            'n=5',
            'address=bY13xeAjLrsjP4KGETwStK2a9UgKgXVTXu'
        ]
        test_r = {
            'b64address': 'VdNmakxFORPSyfCprAD/eDDPk5TY9QYtSA==',
            'name': 'test',
            'amount': 5.3,
            'n': 5,
            'address': 'bY13xeAjLrsjP4KGETwStK2a9UgKgXVTXu'
        }
        self.assertDictEqual(test_r, DaemonCLI.get_params_from_kwargs(test_params))
