import * as rp from 'request-promise';
import { IContact } from './IContact';
import { IContactRequestOptions } from './IContactRequestOptions';
import { IPostContactResponse } from './IPostContactResponse';
import { IPutContactResponse } from './IPutContactResponse';

const BASE_URI = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/contacts/';

export async function getContacts(
    options: Partial<IContactRequestOptions>,
): Promise<IContact[]> {
    return await rp(
        mapRequestOptionsToHttpRequestOptions(options, BASE_URI),
    ) as IContact[];
}

export async function postContact(
    options: Partial<IContactRequestOptions>,
): Promise<IPostContactResponse> {
    return await rp.post(
        mapRequestOptionsToHttpRequestOptions(options, BASE_URI),
    ) as IPostContactResponse;
}

export async function putContact(
    options: Partial<IContactRequestOptions>,
    contactId: string,
): Promise<IPutContactResponse> {
    return await rp.put(
        mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`),
    ) as IPutContactResponse;
}

export async function getContact(
    options: Partial<IContactRequestOptions>,
    contactId: string,
): Promise<IContact> {
    return await rp(
        mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`),
    ) as IContact;
}

export async function deleteContact(
    options: Partial<IContactRequestOptions>,
    contactId: string,
): Promise<void> {
    await rp.del(
        mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`));
}

function mapRequestOptionsToHttpRequestOptions(
    options: Partial<IContactRequestOptions>,
    uri: string,
) {
    const { accessToken, thirdPartyAccessId, requestId, deviceId,
        apiRegistrationId, applicationId, maxResponseItems, fromLastUpdatedDate,
        offset, sortBy, orderBy, body,
    } = options;

    return {
        uri,
        headers: {
            accessToken: `Bearer ${accessToken}`,
            thirdPartyAccessId,
            requestId,
            deviceId,
            apiRegistrationId,
            applicationId,
        },
        qs: {
            maxResponseItems,
            fromLastUpdatedDate,
            offset,
            sortBy,
            orderBy,
        },
        body,
        json: true,
    };
}
