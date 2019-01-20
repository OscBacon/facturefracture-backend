"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const rp = require("request-promise");
const Encoder_1 = require("./Encoder");
const BASE_URI = 'https://gateway-web.beta.interac.ca/publicapi/api/v1/access-tokens';
const encoder = new Encoder_1.Encoder();
function getAccessToken(options) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const { unencryptedSecretKey, salt, thirdPartyAccessId } = options;
        return yield rp({
            uri: BASE_URI,
            headers: {
                secretKey: encoder.encode(unencryptedSecretKey, salt),
                salt,
                thirdPartyAccessId,
            },
            json: true,
        });
    });
}
exports.getAccessToken = getAccessToken;
//# sourceMappingURL=request.js.map