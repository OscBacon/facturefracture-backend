import { magenta } from 'colors';
import { config } from 'dotenv';
import { name } from 'faker';
import { inspect, isNullOrUndefined } from 'util';
import { contactBodyType } from './api/contact';
import {
  deleteContact,
  getContact,
  postContact,
  putContact,
} from './api/contact/request';
import { getBasicOptions } from './authenticate';

export function generateContact(): contactBodyType {
  config();

  const contactName = isNullOrUndefined(process.env.CONTACT_NAME)
    ? name.findName()
    : process.env.CONTACT_NAME;
  const contactEmail = isNullOrUndefined(process.env.CONTACT_EMAIL)
    ? 'nodeSamples@beta.inter.ac'
    : process.env.CONTACT_EMAIL;

  return {
    contactName,
    language: 'en',
    notificationPreferences: [
      {
        handle: contactEmail,
        handleType: 'email',
        active: true,
      },
    ],
  };
}

/**
 * Example usage of creating a contact, updating it, viewing it, and deleting it
 */
export const useContacts = async () => {
  config();

  const model = generateContact();

  console.log(magenta('Adding Contact'));
  const createContactResponse = await createContact(model);
  log(createContactResponse);

  console.log(magenta('Retrieving Contact'));
  const contact = await retrieveContact(createContactResponse.contactId);
  log(contact);

  console.log(magenta('Modifying Contact'));
  await modifyContact(contact, contact.contactId);
  const modifiedContact = await retrieveContact(
    createContactResponse.contactId,
  );
  log(modifiedContact);

  console.log(magenta('Deleting Contact'));
  await removeContact(modifiedContact.contactId);
  console.log(magenta('Contact Deleted'));
};

export async function createContact(contact: contactBodyType) {
  const options = await getBasicOptions();
  options.body = contact;

  return postContact(options);
}

export async function modifyContact(
  contact: contactBodyType,
  contactId: string,
) {
  const options = await getBasicOptions();
  options.body = contact;

  return putContact(options, contactId);
}

export async function retrieveContact(contactId: string) {
  const options = await getBasicOptions();

  return getContact(options, contactId);
}

export async function removeContact(contactId: string) {
  const options = await getBasicOptions();

  return deleteContact(options, contactId);
}

// tslint:disable-next-line:no-any
function log(x: any) {
  console.log(inspect(x, { colors: true, depth: null }));
}

if (isMainProcess()) {
  useContacts();
}

function isMainProcess() {
  return require.main === module;
}
