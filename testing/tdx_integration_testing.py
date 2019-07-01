import unittest
import json
from datetime import datetime as dt
from tdxlib import tdx_integration
import os


class TdxTesting(unittest.TestCase):
    timestamp = dt.today().strftime("%d-%B-%Y %H:%M:%S")

    # Create TDXIntegration object for testing use. Called before testing methods.
    def setUp(self):
        testing_vars_file = 'testing_vars.json'
        self.tdx = tdx_integration.TDXIntegration()
        right_now = dt.today()
        if os.path.isfile(testing_vars_file):
            with open(testing_vars_file, 'r') as f:
                self.testing_vars = json.load(f)
        else:
            print('Testing variables need to be populated in file "testing_vars.json" in the working directory.',
                  'A sample file is available in testing/sample_testing_vars. Any *.json files are ignored by git.')

    def test_authentication(self):
        self.assertGreater(len(self.tdx.token), 200)

    def test_get_location_by_id(self):
        standard = self.testing_vars['location']
        test = self.tdx.get_location_by_id(standard['ID'])
        self.assertTrue(test)
        self.assertEqual(test['Name'], standard['Name'])

    def test_get_account_by_id(self):
        standard = self.testing_vars['account']
        test = self.tdx.get_account_by_id(standard['ID'])
        self.assertTrue(test)
        self.assertEqual(test['Name'], standard['Name'])

    def test_get_group_by_id(self):
        standard = self.testing_vars['group']
        test = self.tdx.get_group_by_id(standard['ID'])
        self.assertTrue(test)
        self.assertEqual(test['Name'], standard['Name'])

    def test_get_person_by_uid(self):
        standard = self.testing_vars['person1']
        test = self.tdx.get_person_by_uid(standard['UID'])
        self.assertTrue(test)
        self.assertEqual(test['PrimaryEmail'], standard['PrimaryEmail'])

    def test_get_group_members_by_id(self):
        test = self.tdx.get_group_members_by_id(self.testing_vars['group']['ID'])
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test), 2)

    def test_search_people_name(self):
        standard = self.testing_vars['person1']
        test = self.tdx.get_person_by_name_email(standard['FullName'])
        self.assertEqual(test['UID'], standard['UID'])

    def test_search_people_email(self):
        standard = self.testing_vars['person1']
        test = self.tdx.get_person_by_name_email(standard['PrimaryEmail'])
        self.assertEqual(test['UID'], standard['UID'])

    def test_get_all_accounts(self):
        test = self.tdx.get_all_accounts()
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test), 2)

    def test_get_account_by_name(self):
        standard = self.testing_vars['account']
        test = self.tdx.get_account_by_name(standard['Name'])
        self.assertEqual(test['ID'],standard['ID'])

    def test_get_account_by_name_partial(self):
        standard = self.testing_vars['account']
        test = self.tdx.get_account_by_name(standard['PartialName'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_all_groups(self):
        test = self.tdx.get_all_groups()
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test), 2)

    def test_get_group_by_name(self):
        standard = self.testing_vars['group']
        test= self.tdx.get_group_by_name(standard['Name'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_group_by_name_partial(self):
        standard = self.testing_vars['group']
        test = self.tdx.get_group_by_name(standard['PartialName'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_group_members_by_name(self):
        standard = self.testing_vars['group']
        test = self.tdx.get_group_members_by_name(standard['Name'])
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test),2)

    def test_get_all_custom_attributes(self):
        test = self.tdx.get_all_custom_attributes(self.tdx.component_ids['ticket'])
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test), 2)

    def test_get_ca_by_name(self):
        standard = self.testing_vars['ticket_ca']
        type_id = self.tdx.component_ids[standard['type']]
        test = self.tdx.get_custom_attribute_by_name(standard['Name'], type_id)
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_ca_value_by_name(self):
        ca_standard = self.testing_vars['ticket_ca']
        standard = ca_standard['choice']
        type_id = self.tdx.component_ids[ca_standard['type']]
        ca = self.tdx.get_custom_attribute_by_name(ca_standard['Name'], type_id)
        test = self.tdx.get_custom_attribute_value_by_name(ca, standard['Name'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_all_locations(self):
        test = self.tdx.get_all_locations()
        self.assertTrue(isinstance(test, list))
        self.assertGreaterEqual(len(test), 2)

    def test_get_location_by_name(self):
        standard = self.testing_vars['location']
        test = self.tdx.get_location_by_name(standard['Name'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_location_by_name_partial(self):
        standard = self.testing_vars['location']
        test = self.tdx.get_location_by_name(standard['PartialName'])
        self.assertEqual(test['ID'], standard['ID'])

    def test_get_room_by_name(self):
        location = self.testing_vars['location']
        standard = self.testing_vars['room']
        test_location = self.tdx.get_location_by_name(location['Name'])
        test_room = self.tdx.get_room_by_name(test_location, standard['Name'])
        self.assertEqual(test_room['ID'], standard['ID'])

    def test_get_room_by_partial_name(self):
        location = self.testing_vars['location']
        standard = self.testing_vars['room']
        test_location = self.tdx.get_location_by_name(location['Name'])
        test_room = self.tdx.get_room_by_name(test_location, standard['PartialName'])
        self.assertEqual(test_room['ID'], standard['ID'])

    def test_create_account(self):
        if not self.tdx.sandbox:
            return
        name = 'Testing Account ' + TdxTesting.timestamp
        additional_info = {'Address1': '123 Main Street'}
        ca = self.testing_vars['account_ca']
        custom_attributes = {ca['Name']:ca['choice']['Name']}
        account = self.tdx.create_account(name, True, self.tdx.username, additional_info,
                                          custom_attributes)
        self.assertEqual(account['Address1'], additional_info['Address1'])
        self.assertEqual(account['Attributes'][0]['Value'], str(ca['choice']['ID']))
        self.assertEqual(account['Name'], name)

    def test_edit_account(self):
        if not self.tdx.sandbox:
            return

        # This will fail if test_create_account fails
        name = 'Testing Account ' + TdxTesting.timestamp
        changed_attributes = {'Name': 'Edited Account' + TdxTesting.timestamp}
        edited_account = self.tdx.edit_account(name, changed_attributes)
        self.assertEqual(edited_account['Name'], changed_attributes['Name'])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TdxTesting)
    unittest.TextTestRunner(verbosity=2).run(suite)
