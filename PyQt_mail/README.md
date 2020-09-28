# Mail Transactions with Python + PyQt 

**First of all, you have to open less secure apps for your gmail account. Account Settings > Security > Less Secure Apps.**


To login your mail address change:
```python
username = 'YOUR_MAIL_ADDRESS'
password = 'YOUR_MAIL_PASSWORD'
```

There is a dict called 'blank_mail'. This is what will be seen if you don't have an unseen mail. You can also set those for yourself.

On body part, the text shown is plain text. If you receive a mail written in html, you won't be able to see it.
Although, you can just add an extra if statement in 'for part in ...' as in the following:
```python
if part.get_content_type() == 'text/html':
	email_data['Body'] = part.get_payload(decode=False)
```

In send_mail function, there are constant variables as text which is set to "Email body". If you want to send a mail, if you don't type any letter in the text section, this is what the receiver will see.
```python
def send_mail(text="Email body", subject="Hello World", from_email="YOUR_MAIL_ADDRESS", to_email=None):
```

**In Inbox tab, for each unseen mail in your inbox you need to hit 'Search For Unseen Mail' button.**

**PyQt is just for sending text mails to only one person. If you want to use python file only, you can add images or files as you need.**
**And you can send your mail to several people by giving 'to_email' as a string list.** *(As in ['abc@aaa.com', '123@bbb.com'])*

