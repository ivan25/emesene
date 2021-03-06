'''emesene's notification system'''
from e3 import status
import extension

import logging
log = logging.getLogger('gui.gtkui.Notification')

#TODO add config
#TODO update multiple message on notification
class Notification():
    '''emesene's notification system'''
    NAME = 'Notification'
    DESCRIPTION = 'Emesene\'s notification system'
    AUTHOR = 'Cando'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session):
        """
        Class Constructor
        """
        self.session = session
        self.session.config.get_or_set('b_notify_contact_online', True)
        self.session.config.get_or_set('b_notify_contact_offline', True)
        self.session.config.get_or_set('b_notify_receive_message', True)
        
        self.notifier = extension.get_default('notificationGUI')

        if self.session:
            self.session.signals.conv_message.subscribe(
                self._on_message)
            self.session.signals.contact_attr_changed.subscribe(
                self._on_contact_attr_changed)

    def _on_message(self, cid, account, msgobj, cedict=None):
        """ 
        This is called when a new message arrives to a user.
        """
        #TODO don't notify if the conversation is on focus
        if self.session.config.b_notify_receive_message:
            contact = self.session.contacts.get(account)
            self._notify(contact, contact.nick , msgobj.body)

    def _on_contact_attr_changed(self, account, change_type, old_value,
            do_notify=True):
        """
        This is called when an attribute of a contact changes
        """
        if change_type != 'status':
            return

        contact = self.session.contacts.get(account)
        if not contact:
            return

        if contact.status == status.ONLINE:
            if self.session.config.b_notify_contact_online:
                text = _('is online')
                self._notify(contact, contact.nick, text)
        elif contact.status == status.OFFLINE:
            if self.session.config.b_notify_contact_offline:
                text = _('is offline')
                self._notify(contact, contact.nick, text)

    def _notify(self, contact, title, text):
        """
        This creates and shows the nofification
        """
        if contact.picture is not None:
            uri = "file://" + contact.picture
        else:
            uri = "notification-message-IM"

        self.notifier(title, text, uri)
        