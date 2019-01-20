## Setup

Make a `.env` file in root with the following items and fill in the fields with your credentials. If you fill in `CONTACT_EMAIL`, you must ensure that email is within the `beta.inter.ac` domain or is whitelisted on your account.

```env
# Mandatory Parameters
UNENCRYPTED_SECRET_KEY=
SALT=
THIRD_PARTY_ACCESS_ID=
API_REGISTRATION_ID=
REQUEST_ID=
DEVICE_ID=

# Optional Parameters
ACCESS_TOKEN=
CONTACT_NAME=
CONTACT_EMAIL=
```

## Installing
`npm install`

## Building
`npm run build`


## Running
Make sure you run the build command before using any of these commands.

* `npm run auth` for access tokens
* `npm run contact` for doing contact flow
* `npm run remove-all-contacts` to remove all your contacts
* `npm run request-money` to request money

Note you can change your `.env` file and NOT rerun the `npm run build` command (basically not have to recompile) to be able to use these commands.
