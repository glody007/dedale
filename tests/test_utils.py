import unittest
from app.utils import dict_contient, create_object_from_dico
from app.models import School

class UtilTestCase(unittest.TestCase):

    def setUp(self):
        self.identity = {
                         'first_name' : 'richard',
                         'last_name' : 'dawkins',
                         'age' : 77
                        }

        self.true_identity = {
                              'first_name' : 'richard',
                              'last_name' : 'dawkins',
                              'age' : 77
                             }

        self.fake_identity = {
                              'first_name' : 'richard',
                              'last_name' : 'daw',
                              'age' : 71
                             }

        self.wrong_key_identity = {
                                   'first_name' : 'richard',
                                   'last_name' : 'dawkins',
                                   'ag' : 71
                                  }

    def test_dict_contient(self):
        identity = self.identity
        true_identity = self.true_identity
        fake_identity = self.fake_identity
        wrong_key_identity = self.wrong_key_identity

        identy_egal_true_identy = dict_contient(identity, true_identity)
        self.assertTrue(identy_egal_true_identy)

        identity_egal_fake_identity = dict_contient(identity, fake_identity)
        self.assertFalse(identity_egal_fake_identity)

        identity_egal_fake_identity = dict_contient(identity, fake_identity)
        self.assertFalse(identity_egal_fake_identity)

        identity_egal_wrong_key_identity = dict_contient(identity, wrong_key_identity)
        self.assertFalse(identity_egal_wrong_key_identity)

    def test_create_object_from_dico(self):

        class Identity:
            first_name = ""
            last_name = ""
            age = 0

        identity_datas = self.identity
        wrong_key_identity = self.wrong_key_identity

        with self.assertRaises(KeyError):
            identity = create_object_from_dico(Identity, wrong_key_identity)

        try:
            good_identity = create_object_from_dico(Identity, identity_datas)
        except KeyError:
            good_identity = None

        self.assertTrue(good_identity is not None,
                        "with good dict it doesn't create object")
