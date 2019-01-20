export interface IAccessTokenRequestOptions {
    readonly unencryptedSecretKey: string;
    readonly salt: string;
    readonly thirdPartyAccessId: string;
}
