#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_endem
----------------------------------

Tests for `endem` module.
"""

import pytest

import smtplib

from endem import endem


@pytest.fixture
def emaillib_gmail():
    return endem.EmailSender('gmail')


@pytest.fixture
def emaillib_yandex():
    return endem.EmailSender('yandex')


@pytest.fixture
def emaillib_mail_ru():
    return endem.EmailSender('mail_ru')


def test_emaillib_init():
    '''
    Инициализация библиотеки
    '''
    assert endem.EmailSender('gmail')


def test_emaillib_wrong_init():
    '''
    Инициализация библиотеки без параметров
    '''
    with pytest.raises(TypeError):
        endem.EmailSender()


def test_emaillib_wrong_provider_init():
    '''
    Инициализация библиотеки c неверным провайдером
    '''
    with pytest.raises(endem.EmailSenderError) as excinfo:
        endem.EmailSender('wrong_provider')
    assert 'Invalid provider' in str(excinfo.value)


class TestGmailSend:
    sender_email = 'user@gmail.com'
    sender_password = 'secret'
    to_email = 'user@gmail.com'

    def test_send_with_wrong_to_email(self, emaillib_gmail):
        '''
        Отправка письма с неверным email получателя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_gmail.send(
                'email@example.com', 'password',
                'wrong',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_with_wrong_from_email(self, emaillib_gmail):
        '''
        Отправка письма с неверным email отправителя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_gmail.send(
                'wrong', 'password',
                'email@example.com',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_email(self, emaillib_gmail):
        '''
        Отправка письма
        '''
        assert emaillib_gmail.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!', 'message'
        )

    def test_send_email_to_multi_receivers(self, emaillib_gmail):
        '''
        Отправка письма нескольким получателям
        '''
        assert emaillib_gmail.send(
            self.sender_email, self.sender_password,
            [self.to_email, 'user@example.com'],
            'From test run!', 'message'
        )

    def test_send_email_with_markdown(self, emaillib_gmail):
        '''
        Отправка письма в формате markdown
        '''
        res = emaillib_gmail.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!',
            '# Title\n\ntext `code`'
        )
        assert res.get('body') == (
            '<h1>Title</h1>\n'
            '<p>text <code>code</code></p>'
        )

    def test_send_email_with_wrong_password(self, emaillib_gmail):
        '''
        Отправка письма c неверным паролем
        '''
        with pytest.raises(smtplib.SMTPAuthenticationError) as excinfo:
            emaillib_gmail.send(
                self.sender_email, 'wrong_password',
                self.to_email,
                'From test run!', 'message'
            )
        assert 'Username and Password not accepted' in str(excinfo.value)


class TestYandexSend:
    sender_email = 'user@yandex.ru'
    sender_password = 'secret'
    to_email = 'user@yandex.ru'

    def test_send_with_wrong_to_email(self, emaillib_yandex):
        '''
        Отправка письма с неверным email получателя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_yandex.send(
                'email@example.com', 'password',
                'wrong',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_with_wrong_from_email(self, emaillib_yandex):
        '''
        Отправка письма с неверным email отправителя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_yandex.send(
                'wrong', 'password',
                'email@example.com',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_email(self, emaillib_yandex):
        '''
        Отправка письма
        '''
        assert emaillib_yandex.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!', 'message'
        )

    def test_send_email_to_multi_receivers(self, emaillib_yandex):
        '''
        Отправка письма нескольким получателям
        '''
        assert emaillib_yandex.send(
            self.sender_email, self.sender_password,
            [self.to_email, 'user@example.com'],
            'From test run!', 'message'
        )

    def test_send_email_with_markdown(self, emaillib_yandex):
        '''
        Отправка письма в формате markdown
        '''
        res = emaillib_yandex.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!',
            '# Title\n\ntext `code`'
        )
        assert res.get('body') == (
            '<h1>Title</h1>\n'
            '<p>text <code>code</code></p>'
        )

    def test_send_email_with_wrong_password(self, emaillib_yandex):
        '''
        Отправка письма c неверным паролем
        '''
        with pytest.raises(smtplib.SMTPAuthenticationError) as excinfo:
            emaillib_yandex.send(
                self.sender_email, 'wrong_password',
                self.to_email,
                'From test run!', 'message'
            )
        assert 'Invalid user or password!' in str(excinfo.value)


class TestMailRuSend:
    sender_email = 'user@mail.ru'
    sender_password = 'secret'
    to_email = 'user@mail.ru'

    def test_send_with_wrong_to_email(self, emaillib_mail_ru):
        '''
        Отправка письма с неверным email получателя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_mail_ru.send(
                'email@example.com', 'password',
                'wrong',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_with_wrong_from_email(self, emaillib_mail_ru):
        '''
        Отправка письма с неверным email отправителя
        '''
        with pytest.raises(endem.EmailSenderError) as excinfo:
            emaillib_mail_ru.send(
                'wrong', 'password',
                'email@example.com',
                'subject', 'message'
            )
        assert 'invalid email' in str(excinfo.value)

    def test_send_email(self, emaillib_mail_ru):
        '''
        Отправка письма
        '''
        assert emaillib_mail_ru.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!', 'message'
        )

    def test_send_email_to_multi_receivers(self, emaillib_mail_ru):
        '''
        Отправка письма нескольким получателям
        '''
        assert emaillib_mail_ru.send(
            self.sender_email, self.sender_password,
            [self.to_email, 'user@example.com'],
            'From test run!', 'message'
        )

    def test_send_email_with_markdown(self, emaillib_mail_ru):
        '''
        Отправка письма в формате markdown
        '''
        res = emaillib_mail_ru.send(
            self.sender_email, self.sender_password,
            self.to_email,
            'From test run!',
            '# Title\n\ntext `code`'
        )
        assert res.get('body') == (
            '<h1>Title</h1>\n'
            '<p>text <code>code</code></p>'
        )

    def test_send_email_with_wrong_password(self, emaillib_mail_ru):
        '''
        Отправка письма c неверным паролем
        '''
        with pytest.raises(smtplib.SMTPAuthenticationError) as excinfo:
            emaillib_mail_ru.send(
                self.sender_email, 'wrong_password',
                self.to_email,
                'From test run!', 'message'
            )
        assert 'Authentication failed.' in str(excinfo.value)
