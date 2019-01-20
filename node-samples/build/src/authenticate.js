"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const dotenv_1 = require("dotenv");
const util_1 = require("util");
const access_token_1 = require("./api/access_token");
exports.authenticate = () => tslib_1.__awaiter(this, void 0, void 0, function* () {
    dotenv_1.config();
    const requestAccessTokenOptions = {
        unencryptedSecretKey: process.env.UNENCRYPTED_SECRET_KEY,
        salt: process.env.SALT,
        thirdPartyAccessId: process.env.THIRD_PARTY_ACCESS_ID,
    };
    const accessToken = yield access_token_1.getAccessToken(requestAccessTokenOptions);
    if (isMainProcess()) {
        console.log(util_1.inspect(accessToken, { colors: true, depth: null }));
    }
    return accessToken;
});
function getBasicOptions() {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        return {
            accessToken: yield getAccessToken(),
            thirdPartyAccessId: process.env.THIRD_PARTY_ACCESS_ID,
            requestId: process.env.REQUEST_ID,
            deviceId: process.env.DEVICE_ID,
            apiRegistrationId: process.env.API_REGISTRATION_ID,
            applicationId: process.env.APPLICATION_ID,
            body: undefined,
        };
    });
}
exports.getBasicOptions = getBasicOptions;
function getAccessToken() {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const accessToken = process.env.ACCESS_TOKEN;
        if (util_1.isNullOrUndefined(accessToken)) {
            return (yield exports.authenticate()).access_token;
        }
        return accessToken;
    });
}
exports.getAccessToken = getAccessToken;
if (isMainProcess()) {
    exports.authenticate();
}
function isMainProcess() {
    return require.main === module;
}
//# sourceMappingURL=authenticate.js.map