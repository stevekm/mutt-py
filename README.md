# mutt-py
A Python wrapper script for emailing with the `mutt` [program](http://www.mutt.org/).

This script will let you easily send a message from your remote server with multiple files attached, avoiding the need to download files to your local machine in order to email them. 

# Usage
The only required flag is `-r` to specify a list of email recipients. Other flags can be provided, to fill in the subject line, body message, and reply-to address. Any extra positional arguments are treated as files to be attached. 

```bash
$ ./mutt.py -s "Merry Christmas!" -r "mom@internets.com, dad@internets.com" -rt "steve@internets.com" -m "Merry Christmas, Mom and Dad! Love, Steve" christmas_card.txt presents.txt
```
Output:
```
Email command is:

export EMAIL="steve@internets.com"

mutt -s "Merry Christmas" -a "christmas_card.txt" -a "presents.txt"  -- "mom@internets.com, dad@internets.com" <<E0F
Merry Christmas, Mom and Dad! Love, Steve
E0F

Running command, sending email...
```

The script will run the `mutt` command as shown, sending the email with specified attachments and recipients. 

This can be combined with the `find` command to search your system for desired files to be emailed:
```
$ find . -maxdepth 1 -type f | xargs ./mutt.py -r "kellys04@nyumc.org"
Email command is:

export EMAIL=""

mutt -s "[mutt.py]" -a "./README.md" -a "./christmas_card.txt" -a "./presents.txt" -a "./mutt.py"  -- "kellys04@nyumc.org" <<E0F
~ This message was sent by the mutt.py email script ~
E0F

Running command, sending email...
```

# Notes

Currently, newline characters are not rendered properly when using the `-m` argument. If your message requires newlines, then consider using the `-mf` argument to send the contents of a file as the message instead. 

```
$ cat message.txt
This is the email message
I wrote this message
to be sent in the email
- Stephen

$ ./mutt.py -r "kellys04@nyumc.org" -mf message.txt
Email command is:

export EMAIL=""

mutt -s "[mutt.py]"  -- "kellys04@nyumc.org" <<E0F
This is the email message
I wrote this message
to be sent in the email
- Stephen


E0F

Running command, sending email...
```

If you need to generate the contents of such a message dynamically, consider using a heredoc for message generation as well:

```bash
message_file="message2.txt"
foo="fooooo"
bar="baaaar"

cat > "$message_file" <<E02
$foo
$bar
E02

./mutt.py -r "kellys04@nyumc.org" -mf "$message_file"
```

```
Email command is:

export EMAIL=""

mutt -s "[mutt.py]"  -- "kellys04@nyumc.org" <<E0F
fooooo
baaaar

E0F

Running command, sending email...
```

## Why `mutt-py`?

While Python does have a built in email library, `mutt` is a very robust program that requires less configuration to use and is easily available on most Linux systems. On OS X, you can download it with homebrew with the command `brew install mutt`. 

The main drawback to `mutt`, and the reason for this script, is that `mutt`'s required syntax is difficult to expand dynamically for variable numbers of file attachments. 

# Software Requirements
this script was developed & tested with the following:
- Python 2.6, 2.7, 3.4.3
- bash version 4.1.2
- Mutt 1.5.20
