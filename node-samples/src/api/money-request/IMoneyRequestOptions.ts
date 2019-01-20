import { IMoneyRequest } from './IMoneyRequest';

type orderingStrategy = 'asc' | 'dsc';

export interface IMoneyRequestOptions {
  accessToken: string;
  thirdPartyAccessId: string;
  requestId: string;
  deviceId: string;
  apiRegistrationId?: string;
  applicationId?: string;
  maxResponseItems?: number;
  fromDate?: string;
  toDate?: string;
  offset?: number;
  sortBy?: 'creationDate';
  orderBy?: orderingStrategy;
  sourceMoneyRequestId?: string;
  referenceNumber?: string;
  body: IMoneyRequest;
}
