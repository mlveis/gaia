# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: 40 minutes

import time

from gaiatest import GaiaEnduranceTestCase
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts


class TestEnduranceAddContact(GaiaEnduranceTestCase):

    def setUp(self):
        GaiaEnduranceTestCase.setUp(self)
        self.contacts = Contacts(self.marionette)
        self.contacts.launch()

    def test_endurance_add_contact(self):
        self.drive(test=self.add_contact, app='contacts')

    def add_contact(self):
        # Add a new contact, most of this code borrowed from test_add_new_contact
        # Uses data from mock contact, except adds iteration to first name

        # Add new contact
        new_contact_form = self.contacts.tap_new_contact()

        # Enter data into fields
        contact = MockContact()
        contact['givenName'] = "%02dof%02d" % (self.iteration, self.iterations)
        new_contact_form.type_given_name(contact['givenName'])
        new_contact_form.type_family_name(contact['familyName'])
        new_contact_form.type_phone(contact['tel'][0]['value'])
        new_contact_form.type_email(contact['email'][0]['value'])
        new_contact_form.type_street(contact['adr'][0]['streetAddress'])
        new_contact_form.type_zip_code(contact['adr'][0]['postalCode'])
        new_contact_form.type_city(contact['adr'][0]['locality'])
        new_contact_form.type_country(contact['adr'][0]['countryName'])
        new_contact_form.type_comment(contact['note'])

        # Save new contact
        new_contact_form.tap_done()
        time.sleep(2)

        # Ensure all contacts were added
        if self.iteration == self.iterations:
            self.assertEqual(len(self.contacts.contacts), self.iterations)

        # Sleep between reps
        time.sleep(3)
