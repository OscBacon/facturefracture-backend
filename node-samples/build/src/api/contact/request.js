"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const rp = require("request-promise");
const BASE_URI = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/contacts/';
function getContacts(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return yield rp(mapRequestOptionsToHttpRequestOptions(options, BASE_URI));
    });
}
exports.getContacts = getContacts;
function postContact(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return yield rp.post(mapRequestOptionsToHttpRequestOptions(options, BASE_URI));
    });
}
exports.postContact = postContact;
function putContact(options, contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return yield rp.put(mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`));
    });
}
exports.putContact = putContact;
function getContact(options, contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return yield rp(mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`));
    });
}
exports.getContact = getContact;
function deleteContact(options, contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        yield rp.del(mapRequestOptionsToHttpRequestOptions(options, `${BASE_URI}${contactId}`));
    });
}
exports.deleteContact = deleteContact;
function mapRequestOptionsToHttpRequestOptions(options, uri) {
    const { accessToken, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, applicationId, maxResponseItems, fromLastUpdatedDate, offset, sortBy, orderBy, body, } = options;
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
//# sourceMappingURL=request.js.map