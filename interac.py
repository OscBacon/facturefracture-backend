import requests
import os
import datetime

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

'''
 * [sendMoneyRequest creates a money request for an e-Transfer customer]
 * param  string accessToken                   [OAuth2 access token, the format is 'Bearer AccessToken']
 * param  string thirdPartyAccessid            [unique id that identifies a third party partner]
 * param  string requestId                     [partner generated unique id for each request used for message tracking purposes]
 * param  string deviceId                      [user device unique identifier]
 * param  string applicationId                 [user application unique identifier]
 * param  string apiRegistrationId             [unique identifier for the user api registration]
 * param  string referenceNumber               [unique identifier for the money request; this field should not be specified in the POST request]
 * param  string sourceMoneyRequestId          [unique identifier of the money request in the originating system (1 to 64 characters length)]
 * param  string requestFromContactId          [Unique identifier for the contact; required for permanent contact]
 * param  string requestFromContactHash        [unique hash value to identify version of contact;required for permanent contact]
 * param  string requestFromContacName         [contact name, required for onetime contact]
 * param  string language                      [language used to notify this contact, required for onetime contact. Values: en, fr]
 * param  string notificationPrefHandle        [Email address (format ab.ca) or mobile phone number ( format 123-222-7777 )]
 * param  string notificationHandleType        [email, sms]
 * param  string active                        [specifies if notifications will not be sent]
 * param  string amount                        [the requested amount (it will be converted into double by the app)]
 * param  string currency                      [the currency of the requested amount; only CAD is supported for now]
 * param  string editableFulfillAmount         [flag indicating if the transfer amount can be different from the requested amount. Values: true, false. TODO: it seems like we can only set this field to false]
 * param  string requesterMessage              [message from the requester. Max length: 400 characters]
 * param  string invoiceNumber                 [number of the invoice to be paid. Max length: 120 characters]
 * param  string dueDate                       [UTC date of the invoice is to be paid by; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * param  string expiryDate                    [UTC datatime this money request is valid until; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * param  string supressResponderNotifications [if flag is on, Interac will not send notifications to the intended responder; the requester is expected to handle the notification part themselves. Values: true, false. Values will be converted into boolean by the web app]
 * param  string returnURL                     [return URL to redirect the Responder after the Money Request fulfillment]
 * param  string creationDate                  [UTC datatime of creation for this request; this field should not be specified in POST or PUT requests; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * param  integer status                       [Does not need to be provided at request creation time; this field should not be specified in POST or PUT requests. Values: REQUEST_INITIATED(1), AVAILABLE_TO_BE_FULFILLED(2), REQUEST_FULFILLED(3), DECLINED(4), CANCELLED(5), EXPIRED(6), DEPOSIT_FAILED(7), REQUEST_COMPLETED(8)]
 * param  string fulfillAmount                 [the fulfilled amount; to not be specified in POST or PUT requests; present if status is completed. It will be converted into double by the web app]
 * param  string responderMessage              [message from the responder; this field should not be specified in POST or PUT requests]
 * param  integer notificationStatus           [indicates the status of the notifications sent to the recipient; this field should not be specified in POST or PUT requests | SENT(0) PENDING(1) PENDING_SEND_FAILURE(2) DELIVERY_FAILURE(3)]
 * return string                                [JSON string containing the unique referenceNumber and the paymentGatewayUrl]

'''


def sendMoneyRequest(user, amount, dinnerdaddy, code,
                     applicationId='string', sourceMoneyRequestId='string', referenceNumber='string',
                     currency='string', editableFulfillAmount=False, requesterMessage='string',
                     invoiceNumber='string', supressResponderNotifications='string',
                     returnURL='string', status='string', fulfillAmount='string',
                     responderMessage='string', notificationStatus='string'):
    os.environ['ACCESS_TOKEN'] = "8b50801e-5ae4-494e-925c-eec9adddbdb8"

    fromDate = datetime.datetime.now().isoformat()[:-3]
    expiryDate = (datetime.datetime.now() + datetime.timedelta(365)).isoformat()[:-3]

    headerBody = {
        'accessToken': 'Bearer ' + os.environ['ACCESS_TOKEN'],
        'thirdPartyAccessId': 'CA1TA8652HQPS3qY',
        'requestId': '4453a5bb-fd72-481f-b796-8efbe43b0d22',
        'deviceId': '49794efc-aefd-4e4c-a4e8-2d013ade09a9',
        'apiRegistrationId': 'CA1AR3HKNc3peBP2'

    }

    dataPassed = {
        "referenceNumber": referenceNumber,
        "sourceMoneyRequestId": 'asfd',
        "requestedFrom": {
            "contactId": 'CArEgVW9BTXu',
            "contactHash": '2214257a5dd76589f1236687548548a2',
            "contactName": user,
            "language": 'en',
            "notificationPreferences": [
                {
                    "handle": "oscar.baracos@gmail.com",
                    "handleType": "email",
                    "active": True
                }
            ]
        },

        "amount": amount,
        "currency": "CAD",
        "editableFulfillAmount": False,
        "requesterMessage": "User {} has requested money from bill {}".format(dinnerdaddy, code),
        "invoice": {
            "invoiceNumber": "string",
            "dueDate": expiryDate
        },

        "expiryDate": expiryDate,
        "supressResponderNotifications": True,
        "returnURL": "string",
        "creationDate": fromDate,
        "status": 0,
        "fulfillAmount": 0,
        "responderMessage": "string",
        "notificationStatus": 0
    }
    response = requests.post(url2 + 'money-requests/send/', headers=headerBody, json=dataPassed)
    print(response.status_code)
    dataRec = response.json()
    print('sendMoneyRequest Data: ')
    print(dataRec)