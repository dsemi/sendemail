#!/usr/bin/python2

import os
import argparse
import sendgrid


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--attachments",
                        help="File(s) to be attached to the email, space separated",
                        nargs="+",
                        default="")
    parser.add_argument("-f", "--sender",
                        help="The email address to send from",
                        required=True)
    parser.add_argument("-s", "--subject",
                        help="Subject of the email",
                        default="")
    parser.add_argument("-m", "--message",
                        help="Body text of the email",
                        default="default")
    parser.add_argument("-t", "--emails",
                        help="The email addresses to send to, space separated",
                        nargs="+",
                        required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    s = sendgrid.Sendgrid(os.environ['SENDGRID_USERNAME'], os.environ['SENDGRID_KEY'], secure=True)
    message = sendgrid.Message(addr_from=args.sender, subject=args.subject, text=args.message)
    for addr in args.emails:
        message.add_to(addr)
    
    # Attachments must be under 7MB in size each, and under 20MB total
    # Should add a check eventually
    for filepath in args.attachments:
        message.add_attachment(os.path.basename(filepath), filepath)
    s.smtp.send(message)


if __name__ == '__main__':
    main()
