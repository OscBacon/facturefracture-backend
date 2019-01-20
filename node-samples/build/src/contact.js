"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const colors_1 = require("colors");
const dotenv_1 = require("dotenv");
const faker_1 = require("faker");
const util_1 = require("util");
const request_1 = require("./api/contact/request");
const authenticate_1 = require("./authenticate");
function generateContact() {
    dotenv_1.config();
    const contactName = util_1.isNullOrUndefined(process.env.CONTACT_NAME)
        ? faker_1.name.findName()
        : process.env.CONTACT_NAME;
    const contactEmail = util_1.isNullOrUndefined(process.env.CONTACT_EMAIL)
        ? 'nodeSamples@beta.inter.ac'
        : process.env.CONTACT_EMAIL;
    return {
        contactName,
        language: 'en',
        notificationPreferences: [
            {
                handle: contactEmail,
                handleType: 'email',
                active: true,
            },
        ],
    };
}
exports.generateContact = generateContact;
exports.useContacts = () => tslib_1.__awaiter(this, void 0, void 0, function* () {
    dotenv_1.config();
    const model = generateContact();
    console.log(colors_1.magenta('Adding Contact'));
    const createContactResponse = yield createContact(model);
    log(createContactResponse);
    console.log(colors_1.magenta('Retrieving Contact'));
    const contact = yield retrieveContact(createContactResponse.contactId);
    log(contact);
    console.log(colors_1.magenta('Modifying Contact'));
    yield modifyContact(contact, contact.contactId);
    const modifiedContact = yield retrieveContact(createContactResponse.contactId);
    log(modifiedContact);
    console.log(colors_1.magenta('Deleting Contact'));
    yield removeContact(modifiedContact.contactId);
    console.log(colors_1.magenta('Contact Deleted'));
});
function createContact(contact) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const options = yield authenticate_1.getBasicOptions();
        options.body = contact;
        return request_1.postContact(options);
    });
}
exports.createContact = createContact;
function modifyContact(contact, contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const options = yield authenticate_1.getBasicOptions();
        options.body = contact;
        return request_1.putContact(options, contactId);
    });
}
exports.modifyContact = modifyContact;
function retrieveContact(contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const options = yield authenticate_1.getBasicOptions();
        return request_1.getContact(options, contactId);
    });
}
exports.retrieveContact = retrieveContact;
function removeContact(contactId) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const options = yield authenticate_1.getBasicOptions();
        return request_1.deleteContact(options, contactId);
    });
}
exports.removeContact = removeContact;
function log(x) {
    console.log(util_1.inspect(x, { colors: true, depth: null }));
}
if (isMainProcess()) {
    exports.useContacts();
}
function isMainProcess() {
    return require.main === module;
}
//# sourceMappingURL=contact.js.map