import { IContact } from './IContact';

type sortingStrategy = 'contactName' | 'contactUpdatedDate';
type orderingStrategy = 'asc' | 'dsc';
export type contactBodyType = Pick<IContact, Exclude<keyof IContact, 'contactHash' | 'contactId'>>;

export interface IContactRequestOptions {
    accessToken: string;
    thirdPartyAccessId: string;
    requestId: string;
    deviceId: string;
    apiRegistrationId?: string;
    applicationId?: string;
    maxResponseItems?: number;
    fromLastUpdatedDate?: string;
    offset?: number;
    sortBy?: sortingStrategy;
    orderBy?: orderingStrategy;
    body?: contactBodyType;
}
