"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const rp = require("request-promise");
const BASE_URI = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/money-requests/';
function postMoneyRequest(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return yield rp.post(mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}/send`));
    });
}
exports.postMoneyRequest = postMoneyRequest;
function mapRequestOptionsToHttpRequestOptions(options, uri) {
    const { accessToken, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, applicationId, maxResponseItems, offset, sortBy, orderBy, body, fromDate, toDate, sourceMoneyRequestId, referenceNumber, } = options;
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
//# sourceMappingURL=request.js.map