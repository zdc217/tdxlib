import unittest
import json
from datetime import datetime as dt
from tdxlib import tdx_ticket_integration


class TdxTicketTesting(unittest.TestCase):

    # Create TDXIntegration object for testing use. Called before testing methods.
    def setUp(self):
        self.tix = tdx_ticket_integration.TDXTicketIntegration()
        right_now = dt.today()
        self.timestamp = right_now.strftime("%d-%B-%Y %H:%M:%S")
        with open('testing_vars.json', 'r') as f:
            self.testing_vars = json.load(f)
    
    def test_authn(self):
        self.assertGreater(len(self.tix.token), 200)

    def test_get_ticket_by_id(self):
        self.assertTrue(self.tix.get_ticket_by_id(self.testing_vars['ticket1']['ID']))  # TDX Test Ticket #5814276

    def test_search_tickets(self):
        self.assertTrue(self.tix.search_tickets('test'))

    # #### CHANGING TICKETS #### #

    def test_edit_tickets(self):
        # Protect production from deleting tasks
        if not self.tix.sandbox:
            return
        ticket_list = list()
        ticket_list.append(self.tix.get_ticket_by_id(self.testing_vars['ticket2']['ID']))
        ticket_list.append(self.tix.get_ticket_by_id(self.testing_vars['ticket3']['ID']))
        title_string = self.timestamp + ' testing ticket'
        changes = {
            'Title': title_string
        }
        changed_tickets = self.tix.edit_tickets(ticket_list, changes, notify=False)
        self.assertTrue(all(changed_tickets))
        for i in changed_tickets:
            self.assertEqual(i.get_attribute('Title'), changes['Title'])

    # #### GETTING TICKET ATTRIBUTES #### #

    def test_get_all_ticket_types(self):
        types = self.tix.get_all_ticket_types()
        self.assertGreaterEqual(len(types), 40)

    def test_get_ticket_type_by_id(self):
        key = self.testing_vars['ticket_type']['ID'] # IT Internal
        self.assertTrue(self.tix.get_ticket_type_by_name_id(key))

    def test_get_ticket_type_by_name(self):
        key = self.testing_vars['ticket_type']['Name']
        self.assertTrue(self.tix.get_ticket_type_by_name_id(key))

    def test_get_all_ticket_statuses(self):
        statuses = self.tix.get_all_ticket_statuses()
        self.assertGreaterEqual(len(statuses), 5)

    def test_get_ticket_status_by_id(self):
        key = self.testing_vars['ticket_status']['ID'] # Open
        self.assertTrue(self.tix.get_ticket_status_by_id(key))

    def test_get_ticket_status_by_name(self):
        key = self.testing_vars['ticket_status']['Name']
        self.assertTrue(self.tix.search_ticket_status(key))

    def test_get_all_ticket_priorities(self):
        priorities = self.tix.get_all_ticket_priorities()
        self.assertGreaterEqual(len(priorities), 4)

    def test_get_ticket_priority_by_id(self):
        key = self.testing_vars['ticket_priority']['ID']  # Low
        self.assertTrue(self.tix.get_ticket_priority_by_name_id(key))

    def test_get_ticket_priority_by_name(self):
        name = self.testing_vars['ticket_priority']['Name']
        self.assertTrue(self.tix.get_ticket_priority_by_name_id(name))

    def test_get_ticket_classification_id_by_name(self):
        name = self.testing_vars['ticket_classification']['Name']
        self.assertTrue(self.tix.get_ticket_classification_id_by_name(name))

    def test_get_all_ticket_urgencies(self):
        urgencies = self.tix.get_all_ticket_urgencies()
        self.assertGreaterEqual(len(urgencies), 3)

    def test_get_ticket_urgency_by_id(self):
        key =  self.testing_vars['ticket_urgency']['ID']
        self.assertTrue(self.tix.get_ticket_urgency_by_name_id(key))

    def test_get_ticket_urgency_by_name(self):
        key = self.testing_vars['ticket_urgency']['Name']
        self.assertTrue(self.tix.get_ticket_urgency_by_name_id(key))

    def test_get_all_ticket_impacts(self):
        impacts = self.tix.get_all_ticket_impacts()
        self.assertGreaterEqual(len(impacts), 5)

    def test_get_ticket_impact_by_id(self):
        key = self.testing_vars['ticket_impact']['ID']
        self.assertTrue(self.tix.get_ticket_impact_by_name_id(key))

    def test_get_ticket_impact_by_name(self):
        key = self.testing_vars['ticket_impact']['Name']
        self.assertTrue(self.tix.get_ticket_impact_by_name_id(key))

    def test_get_all_ticket_sources(self):
        sources = self.tix.get_all_ticket_sources()
        self.assertGreaterEqual(len(sources), 7)

    def test_get_ticket_source_by_id(self):
        key = self.testing_vars['ticket_source']['ID']
        self.assertTrue(self.tix.get_ticket_source_by_name_id(key))

    def test_get_ticket_source_by_name(self):
        key = self.testing_vars['ticket_source']['Name']
        self.assertTrue(self.tix.get_ticket_source_by_name_id(key))

    def test_create_ticket(self):
        # Protect production from testing tickets
        if not self.tix.sandbox:
            return
        else:
            title_string = "Testing Ticket Created " + self.timestamp
            json_data = self.tix.generate_ticket(title_string,
                                                 self.testing_vars['ticket_type']['Name'],
                                                 self.testing_vars['account']['Name'],
                                                 self.tix.username)
            created_ticket = self.tix.create_ticket(json_data)
            self.assertTrue(created_ticket.get_id() > 10000)

    # #### TICKET TASKS #### #

    def test_get_all_tasks_by_ticket_id(self):
        ticket_id = self.testing_vars['ticket2']['ID']
        self.assertTrue(self.tix.get_all_tasks_by_ticket_id(ticket_id))

    def test_get_ticket_task_by_id(self):
        ticket_id = self.testing_vars['ticket2']['ID']
        task_id = self.testing_vars['ticket2']['task']['ID']
        self.assertTrue(self.tix.get_ticket_task_by_id(ticket_id, task_id))

    def test_create_ticket_task(self):
        # Protect production from testing tasks
        if not self.tix.sandbox:
            return
        else:
            ticket_id = self.testing_vars['ticket2']['ID']
            task = {
                'Title': f"Test task at {dt.now()}"
            }
            created_task = self.tix.create_ticket_task(ticket_id, task)
            self.assertGreater(created_task['ID'], 10000)
            self.task_id_to_delete = created_task['ID']

    def test_edit_ticket_task(self):
        # Protect production from deleting tasks
        if not self.tix.sandbox:
            return
        ticket_id = self.testing_vars['ticket2']['ID']
        task_id = self.testing_vars['ticket2']['task']['ID']
        task = self.tix.get_ticket_task_by_id(ticket_id, task_id)
        changed_attributes = {
            'Description': f'This task was updated at {dt.now()}.'
        }
        edited_task = self.tix.edit_ticket_task(ticket_id, task, changed_attributes)
        self.assertTrue(edited_task)
        self.assertEqual(edited_task['Description'], changed_attributes['Description'])

    def test_delete_ticket_task(self):
        if not self.tix.sandbox:
            return
        # Create the task
        ticket_id = self.testing_vars['ticket2']['ID']
        task = {
            'Title': f'Delete this task at {dt.now()}'
        }
        created_task = self.tix.create_ticket_task(ticket_id, task)
        # Delete the task
        self.tix.delete_ticket_task(ticket_id, self.created_task['ID'])
        # Make sure the task is deleted
        deleted_task = self.tix.get_ticket_task_by_id(ticket_id, created_task['ID'])
        self.assertFalse(deleted_task)

    def test_reassign_ticket_task(self):
        ticket_id = self.testing_vars['ticket2']['ID']
        task_id = self.testing_vars['ticket2']['task']['ID']
        task = self.tix.get_ticket_task_by_id(task_id)
        if task['ResponsibleUid'] == self.testing_vars['person1']['UID']:
            reassign = {'ResponsibleUid': self.testing_vars['person2']['UID']}
        else:
            reassign = {'ResponsibleUid': self.testing_vars['person1']['UID']}
        changed_task = self.tix.edit_ticket_task(ticket_id, task_id, reassign)
        self.assertEqual(changed_task['ResponsibleUid'], reassign['ResponsibleUid'])

    # TODO:
    # test_reassign_ticket
    # test_reschedule_ticket
    # test_reassign_ticket_task
    # test_reschedule_ticket_task
    # test_generate_ticket_task
    # test_create_custom_ticket_status
    # test_edit_custom_ticket_status
    # test_update_ticket_task_feed
    # test_get_ticket_task_feed
    # test_get_ticket_feed
    # test_update_ticket_feed


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TdxTicketTesting)
    unittest.TextTestRunner(verbosity=2).run(suite)
