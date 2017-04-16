#!/usr/bin/env python

'''
This script provides a flexible wrapper for mailing files from a remote server with mutt

USAGE: mutt.py -s "Subject line" -r "address1@gmail.com, address2@gmail.com" -rt "my.address@internets.com" -m "This is my email message" /path/to/attachment1.txt /path/to/attahment2.txt

example mutt command which will be created:
# reply-to field; PUT YOUR EMAIL HERE
export EMAIL="kellys04@nyumc.org"
recipient_list="address1@gmail.com, address2@gmail.com"
mutt -s "$SUBJECT_LINE" -a "$attachment_file" -a "$summary_file" -a "$zipfile" -- "$recipient_list" <<E0F
email message HERE
E0F
'''


# ~~~~ LOAD PACKAGES ~~~~~~ #
import sys
import os
import subprocess as sp
import argparse

# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def subprocess_cmd(command):
    '''
    Runs a terminal command with stdout piping enabled
    '''
    import subprocess as sp
    process = sp.Popen(command,stdout=sp.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

def make_attachement_string(attachment_files):
    '''
    Return a string to use to in the mutt command to include attachment files
    ex:
    -a "$attachment_file" -a "$summary_file" -a "$zipfile"
    '''
    attachment_strings = []
    if len(attachment_files) > 0:
        for file in attachment_files:
            file_string = '-a "{0}" '.format(file)
            attachment_strings.append(file_string)
    attachment_string = ''.join(attachment_strings)
    return(attachment_string)

def mutt_mail(recipient_list, reply_to, subject_line, message, attachment_files):
    '''
    Send the message with mutt
    '''
    attachment_string = make_attachement_string(attachment_files)
    command = '''
export EMAIL="{0}"

mutt -s "{1}" {2} -- "{3}" <<E0F
{4}
E0F'''.format(reply_to, subject_line, attachment_string, recipient_list, message) # message.replace('\n', "$'\n'")
    print('Email command is:\n{0}\n'.format(command))
    print('Running command, sending email...')
    subprocess_cmd(command)



# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='Mutt email wrapper')

# required flags
parser.add_argument("-r", type = str, required=True, dest = 'recipient_list', metavar = 'recipient_list', help="Email(s) to be included in the recipient list") # nargs='+'

# optional positional args
parser.add_argument("attachment_files", type = str,  nargs='*', help="Files to be attached to the email") # nargs='+' # default = [],  action='append', nargs='?',

# optional flags
parser.add_argument("-s", default = '[mutt.py]', type = str, dest = 'subject_line', metavar = 'subject_line', help="Subject line for the email")
parser.add_argument("-m", default = '~ This message was sent by the mutt.py email script ~', type = str, dest = 'message', metavar = 'message', help="Message for the body of the email")
parser.add_argument("-rt", default = '', type = str, dest = 'reply_to', metavar = 'message', help="Message for the body of the email")

args = parser.parse_args()

recipient_list = args.recipient_list
attachment_files = args.attachment_files
subject_line = args.subject_line
message = args.message
reply_to = args.reply_to

if __name__ == "__main__":
    mutt_mail(recipient_list = recipient_list, reply_to = reply_to, subject_line = subject_line, message = message, attachment_files = attachment_files)
