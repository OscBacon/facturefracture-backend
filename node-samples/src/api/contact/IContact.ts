import { INotificationPreference } from './INotificationPreference';

export interface IContact {
    contactId?: string;
    contactName?: string;
    contactHash?: string;
    language: 'en' | 'fr';
    notificationPreferences: INotificationPreference[];
}
