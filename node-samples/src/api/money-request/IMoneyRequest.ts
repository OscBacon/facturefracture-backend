import { IContact } from '../contact';

const REQUEST_INITIATED = 1;
const AVAILABLE_TO_BE_FULFILLED = 2;
const REQUEST_FULFILLED = 3;
const DECLINED = 4;
const CANCELLED = 5;
const EXPIRED = 6;
const DEPOSIT_FAILED = 7;
const REQUEST_COMPLETED = 8;
type MoneyRequestStatus
  = typeof REQUEST_INITIATED
  | typeof AVAILABLE_TO_BE_FULFILLED
  | typeof REQUEST_FULFILLED
  | typeof DECLINED
  | typeof CANCELLED
  | typeof EXPIRED
  | typeof DEPOSIT_FAILED
  | typeof REQUEST_COMPLETED;

const SENT = 0;
const PENDING = 1;
const PENDING_SEND_FAILURE = 2;
const DELIVERY_FAILURE = 3;
type NotificationStatus
  = typeof SENT
  | typeof PENDING
  | typeof PENDING_SEND_FAILURE
  | typeof DELIVERY_FAILURE;

export interface IMoneyRequest {
  referenceNumber?: String;
  sourceMoneyRequestId: String;
  requestedFrom: IContact;
  amount: number;
  currency: 'CAD';
  editableFulfillAmount: boolean;
  requesterMessage?: string;
  invoice?: {
    invoiceNumber: string;
    dueDate: string;
  };
  expiryDate: string;
  supressResponderNotifications: boolean;
  returnURL?: string;
  creationDate?: string;
  status?: MoneyRequestStatus;
  fulfillAmount?: number;
  responderMessage?: string;
  notificationStatus?: NotificationStatus;
}
