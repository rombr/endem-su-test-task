# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import click

from endem import EmailSender


@click.command()
@click.option('--provider', default='gmail', help='SMTP provider.')
@click.option('--email', prompt='Your email',
              help='The email account to send.')
@click.option('--password', prompt='Your password',
              help='The password for account to send.',
              hide_input=True)
@click.option('--to', prompt='Reciever(s)',
              help='The Reciever(s) to send.')
@click.option('--subject', prompt='Subject',
              help='The email subject.')
@click.option('--message', prompt='Message',
              help='The message to send.')
def main(provider, email, password, to, subject, message):
    """Console script for endem"""
    EmailSender(provider).send(email, password, to, subject, message)
    click.echo('Message was sent!')


if __name__ == "__main__":
    main()
