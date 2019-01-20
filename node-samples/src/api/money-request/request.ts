import * as rp from 'request-promise';
import { IMoneyRequestOptions } from './IMoneyRequestOptions';
import { IPostMoneyRequestResponse } from './IPostMoneyRequestResponse';

const BASE_URI = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/money-requests/';

export async function postMoneyRequest(
  options: Partial<IMoneyRequestOptions>,
): Promise<IPostMoneyRequestResponse> {
  return await rp.post(
    mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}/send`),
  ) as IPostMoneyRequestResponse;
}

function mapRequestOptionsToHttpRequestOptions(
  options: Partial<IMoneyRequestOptions>,
  uri: string,
) {
  const { accessToken, thirdPartyAccessId, requestId, deviceId,
    apiRegistrationId, applicationId, maxResponseItems,
    offset, sortBy, orderBy, body, fromDate, toDate, sourceMoneyRequestId,
    referenceNumber,
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
      fromDate,
      toDate,
      offset,
      sortBy,
      orderBy,
      sourceMoneyRequestId,
      referenceNumber,
    },
    body,
    json: true,
  };
}
