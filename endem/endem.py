# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
import smtplib
from email.mime.text import MIMEText
import types
import re

import yaml
import markdown


logger = logging.getLogger('emaillib')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


PROVIDERS_CONFIG_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'providers.yml'
)

# Валидация email по мотивам
# https://github.com/syrusakbary/validate_email/blob/master/validate_email.py#L41
WSP = r'[\s]'
CRLF = r'(?:\r\n)'
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'
CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'

COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
    r'?' + QCONTENT + r')*' + FWS + \
    r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'
DOMAIN_LITERAL = (
    CFWS + r'?' + r'\[' +
    r'(?:' + FWS + r'?' + DCONTENT +
    r')*' + FWS + r'?\]' + CFWS + r'?'
)
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN

VALID_ADDRESS_RE = re.compile('^' + ADDR_SPEC + '$')


class EmailSenderError(Exception):
    pass


class EmailSender(object):
    '''
    Отправка email к любому заданному поставщику услуг smtp
    '''
    providers_config_path = PROVIDERS_CONFIG_FILE

    __providers = None

    def __init__(self, provider):
        super(EmailSender, self).__init__()

        if provider not in self.providers:
            raise EmailSenderError('Invalid provider %s!', provider)

        self.provider = provider
        logger.info('Provider is %s', provider)

    def get_providers_config_path(self):
        return self.providers_config_path

    def _validate_providers(self, providers):
        required_fields = (
            'server', 'port',
        )
        for p_name, p_data in providers.items():
            if not all([i in p_data for i in required_fields]):
                raise EmailSenderError(
                    'There are not all required fields for "%s"' % p_name)
        return providers

    @property
    def providers(self):
        '''
        Настройки поставщиков
        '''
        if self.__providers is None:
            with open(self.get_providers_config_path(), 'r') as f:
                self.__providers = self._validate_providers(yaml.load(f))
        return self.__providers

    def validate_email(self, email):
        if VALID_ADDRESS_RE.match(email) is None:
            raise EmailSenderError('invalid email "%s"' % email)
        return email

    def validate_text(self, text):
        return text.strip()

    def process_body(self, text):
        '''
        Преобразование тела письма
        Понимать markdown разметку и транслировать её в html
        '''
        return markdown.markdown(text)

    def send(self, sender_email, sender_password, to, subject, message):
        '''
        Отправить письмо
        '''
        if isinstance(to, types.StringTypes):
            to = [to]

        sender_email = self.validate_email(self.validate_text(sender_email))
        for i in to:
            self.validate_email(i)
        subject = self.validate_text(subject)
        message = self.validate_text(message)

        body = self.process_body(self.validate_text(message))

        logger.info('Prepare message')
        logger.info('from "%s"', sender_email)
        logger.info('to "%s"', to)
        logger.info('with subject "%s"', subject)
        logger.info('and body "%s"', body)

        # > Отправлять как plaintext, так и html
        # Так как при преобразовании текста из markdown в html
        # даже в plain строку добавляются теги p,
        # то это требование теряет смысл,
        # если не вводить параметры формата, обработки markdown
        msg = MIMEText(body, 'html', 'utf-8')

        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ', '.join(to)

        opts = self.providers.get(self.provider)

        logger.info('Open SMTP connection')

        if opts.get('ssl'):
            server = smtplib.SMTP_SSL(
                opts.get('server'), opts.get('port')
            )
        else:
            server = smtplib.SMTP(
                opts.get('server'), opts.get('port')
            )

        logger.info('Sebd SMTP ehlo')
        server.ehlo()

        if opts.get('tls'):
            logger.info('Start TLS')
            server.starttls()
            logger.info('Sebd SMTP ehlo')
            server.ehlo()
        logger.info('Login to SMTP')
        server.login(sender_email, sender_password)

        logger.info('Send email')
        server.sendmail(sender_email, to, msg.as_string())

        logger.info('Close SMTP connection')
        server.quit()

        return dict(
            subject=subject,
            body=body,
        )
