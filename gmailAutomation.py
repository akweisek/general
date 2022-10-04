import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
import email

class AutomateEmail:
    def __init__(self, usr, pwd):
        self.usr = usr
        self.pwd = pwd
        
        self.send_server = smtplib.SMTP('smtp.gmail.com:587')
        self.receive_server = imaplib.IMAP4_SSL('imap.gmail.com',993)
        
    def login(self):
        self.send_server.ehlo_or_helo_if_needed();
        self.send_server.starttls();
        self.send_server.ehlo_or_helo_if_needed();
        self.send_server.login(self.usr,self.pwd)
        
        self.receive_server.login(self.usr,self.pwd)
        
    def logout(self):
        self.send_server.quit()
        self.receive_server.close()
        self.receive_server.logout()
        
        
    def sendEmail(self, to, cc, bcc, subject, msg , attachments = []):
        assert type(self.usr) == str;
        assert type(self.pwd) == str;
        assert type(to) == list;
        assert type(cc) == list;
        assert type(bcc) == list;
        assert type(subject) == str;
        assert type(msg) == str;
        assert type(attachments) == list;
        	
        msg_multipart = MIMEMultipart();
        	
        msg_multipart['From'] = self.usr;
        msg_multipart['To'] = COMMASPACE.join(to);
        msg_multipart['Cc'] = COMMASPACE.join(cc);
        	
        msg_multipart['Date'] = formatdate(localtime = True);
        msg_multipart['Subject'] = subject;
        	
        msg_multipart.attach(MIMEText(msg))
        	
        for f in attachments:
        		part = MIMEBase('application',"octet-stream");
        		part.set_payload(open(f,"rb").read());
        		encoders.encode_base64(part);
        		part.add_header('Content-Disposition','attachment; filename = "%s"' % os.path.basename(f));
        		msg_multipart.attach(part);
                
        self.send_server.sendmail(self.usr, to+cc+bcc, msg_multipart.as_string())
        
    def readEmail(self, param):
        search_criteria = {0: 'ALL',
                           1: 'UNSEEN',
                           2: 'SEEN',
                           3: 'ANSWERED',
                           4: 'UNANSWERED'
                           }
        
        self.receive_server.list();
        self.receive_server.select("inbox")
        
        result, data = self.receive_server.search(None,search_criteria[param])
        ids = data[0];
        ids_list = ids.split();
        
        messages = {};
        source = {};
        to = {};
        cc = {};
        subj = {};
        
        i = len(ids_list)
        
        for j in range(i):
            k = -j-1;
            current_email_id = ids_list[k];
	
            result, data = self.receive_server.fetch(current_email_id, "(RFC822)");
	
            raw_email = data[0][1];
	
            email_message = email.message_from_string(raw_email.decode());
            
            source[j] = email_message['From']
            to[j] = email_message['To']
            cc[j] = email_message['Cc']
            subj[j] = email_message['Subject']
	
            msg_received = [];
	
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    msg_received.append(part.get_payload())
                    
            messages[j] = msg_received;
            
        return messages, source, to, cc, subj