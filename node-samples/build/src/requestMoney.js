"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const colors_1 = require("colors");
const dotenv_1 = require("dotenv");
const moment = require("moment");
const util_1 = require("util");
const uuid_1 = require("uuid");
const request_1 = require("./api/money-request/request");
const authenticate_1 = require("./authenticate");
const contact_1 = require("./contact");
function sendMoney(amount, emailAddress, message) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        dotenv_1.config();
        const requestAmount = (util_1.isNullOrUndefined(process.env.MONEY_REQUEST_AMOUNT)
            ? 100
            : process.env.MONEY_REQUEST_AMOUNT);
        console.log(colors_1.magenta('The following money request will be sent to...'));
        const requestOptions = yield authenticate_1.getBasicOptions();
        console.log(util_1.inspect(contact_1.generateContact(), { colors: true, depth: null }));
        console.log(colors_1.magenta('Sending money request using the following details...'));
        const requestBody = {
            sourceMoneyRequestId: uuid_1.v4().replace(/-/g, ''),
            requestedFrom: contact_1.generateContact(),
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
        console.log(util_1.inspect(requestOptions, { colors: true, depth: null }));
        const moneyRequestResponse = yield request_1.postMoneyRequest(requestOptions);
        console.log(colors_1.magenta('Money Request Details'));
        console.log(util_1.inspect(moneyRequestResponse, { colors: true }));
    });
}
exports.sendMoney = sendMoney;
if (isMainProcess()) {
    sendMoney(100, 'cheryl@beta.inter.ac', 'This is a message!');
}
function isMainProcess() {
    return require.main === module;
}
//# sourceMappingURL=requestMoney.js.map