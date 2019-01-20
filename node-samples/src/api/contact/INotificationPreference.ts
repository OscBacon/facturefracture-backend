export interface INotificationPreference {
    handle: string;
    handleType: 'email' | 'sms';
    active?: boolean;
}
