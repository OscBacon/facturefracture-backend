"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const dotenv_1 = require("dotenv");
const contact_1 = require("./api/contact");
const authenticate_1 = require("./authenticate");
const throttleLimit = 10;
const MILLISECONDS_IN_A_SECOND = 1000;
function removeAllContacts() {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const options = yield authenticate_1.getBasicOptions();
        const contacts = yield contact_1.getContacts(options);
        let counter = 2;
        for (const contact of contacts) {
            yield contact_1.deleteContact(options, contact.contactId);
            counter += 1;
            if (counter % throttleLimit === 0) {
                yield delay(throttleLimit * MILLISECONDS_IN_A_SECOND);
            }
        }
    });
}
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
const main = () => tslib_1.__awaiter(this, void 0, void 0, function* () {
    dotenv_1.config();
    yield removeAllContacts();
});
main();
//# sourceMappingURL=removeAllContacts.js.map