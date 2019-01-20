import { magenta } from 'colors';
import { config } from 'dotenv';
import * as moment from 'moment';
import { inspect, isNullOrUndefined } from 'util';
import { v4 as uuid } from 'uuid';
import { IMoneyRequest } from './api/money-request/IMoneyRequest';
import { postMoneyRequest } from './api/money-request/request';
import { getBasicOptions } from './authenticate';
import { generateContact } from './contact';

export async function sendMoney(amount: number, emailAddress: string, message: string) {
  config();

  const requestAmount = (isNullOrUndefined(process.env.MONEY_REQUEST_AMOUNT)
    ? 100
    : process.env.MONEY_REQUEST_AMOUNT) as number;

  console.log(magenta('The following money request will be sent to...'));
  const requestOptions = await getBasicOptions();
  console.log(inspect(generateContact(), { colors: true, depth: null }));
  console.log(magenta('Sending money request using the following details...'));
  const requestBody: Partial<IMoneyRequest> = {
    sourceMoneyRequestId: uuid().replace(/-/g, ''),
    requestedFrom: generateContact(),
    amount: requestAmount,
    currency: 'CAD',
    editableFulfillAmount: false,
    requesterMessage: message,
    expiryDate: moment()
      .hour(23)
      .minute(59)
      .second(59)
      .utc()
      .toISOString(),
    supressResponderNotifications: false,
  };

  requestOptions.body = requestBody;
  console.log(inspect(requestOptions, { colors: true, depth: null }));

  const moneyRequestResponse = await postMoneyRequest(requestOptions);
  console.log(magenta('Money Request Details'));
  console.log(inspect(moneyRequestResponse, { colors: true }));
}

if (isMainProcess()) {
  sendMoney(100, 'cheryl@beta.inter.ac', 'This is a message!');
}

function isMainProcess() {
  return require.main === module;
}
