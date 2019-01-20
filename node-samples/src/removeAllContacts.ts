import { config } from 'dotenv';
import { deleteContact, getContacts } from './api/contact';
import { getBasicOptions } from './authenticate';

// Max calls per 10 seconds
const throttleLimit = 10;
const MILLISECONDS_IN_A_SECOND = 1000;

async function removeAllContacts() {
  const options = await getBasicOptions();
  const contacts = await getContacts(options);
  let counter = 2;

  for (const contact of contacts) {
    await deleteContact(options, contact.contactId);
    counter += 1;
    if (counter % throttleLimit === 0) {
      await delay(throttleLimit * MILLISECONDS_IN_A_SECOND);
    }
  }
}

function delay(ms: number) {
  // tslint:disable-next-line:typedef
  return new Promise(resolve => setTimeout(resolve, ms));
}

const main = async () => {
  config();
  await removeAllContacts();
};
main();
