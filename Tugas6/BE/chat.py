import base64
import os
from os.path import join, dirname, realpath
import json
import uuid
import logging
from queue import Queue
import threading 
import socket

class RealmBridge(threading.Thread):
    def __init__(self, chat, realm_address_to, realm_port_to, users):
        self.chat = chat
        self.chats = {}
        self.realm_address_to = realm_address_to
        self.realm_port_to = realm_port_to
        self.users = []
        for username in users:
            self.users.append(username)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.realm_address_to, self.realm_port_to))
        threading.Thread.__init__(self)

    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            msg = ""
            while True:
                data = self.sock.recv(1024)
                print("diterima dari server", data)
                if (data):
                    msg = "{}{}" . format(msg, data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
                    if msg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(msg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}
    
    def put(self, message):
        receiver = message['msg_to']
        try:
            self.chats[receiver].put(message)
        except KeyError:
            self.chats[receiver] = Queue()
            self.chats[receiver].put(message)

class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.users['anton'] = { 'name': 'Antonio Taifan', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['cahyadi'] = { 'name': 'Cahyadi Surya', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['frederick'] = { 'name': 'Frederick Wijayadi', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['afdal'] = { 'name': 'Muhammad Afdal', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['ariq'] = { 'name': 'Naufal Ariq', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['marcel'] = { 'name': 'Marcellino Mahesa', 'country': 'Indonesia', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.realms = {}
    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            ## AUTH ##
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                logging.warning("AUTH: auth {} {}" . format(username, password))
                return self.login_user(username, password)
            elif (command == 'register'):
                username = j[1].strip()
                password = j[2].strip()
                name = j[3].strip()
                country = j[4].strip()
                logging.warning("AUTH: register {} {}" . format(username, password))
                return self.register_user(username, password, name, country)
            elif (command == 'logout'):
                session_id = j[1].strip()
                username = self.sessions[session_id]['username']
                logging.warning("AUTH: logout user {}" . format(username))
                return  self.logout_user(session_id)
            
            
            ## INTERNAL SERVER ##
            # PRIVATE            
            elif (command == 'sendprivate'):
                session_id = j[1].strip()
                receiver = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send private message from {} to {}" . format(session_id, sender, receiver))
                return self.send_private_message(session_id, sender, receiver, message)
            elif (command == 'sendprivatefile'):
                session_id = j[1].strip()
                receiver = j[2].strip()
                filename = os.path.basename(j[3].strip())
                encoded_file = j[4].strip()
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send private file {} from {} to {}" . format(session_id, filename, sender, receiver))
                return self.send_private_file(session_id, sender, receiver, filename, encoded_file)
            
            # GROUP
            elif (command == 'sendgroup'):
                session_id = j[1].strip()
                group_receiver = j[2].strip().split(',')
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send message from {} to group {}" . format(session_id, sender, group_receiver))
                return self.send_group_message(session_id, sender, group_receiver, message)
            elif (command == 'sendgroupfile'):
                session_id = j[1].strip()
                group_receiver = j[2].strip().split(',')
                filename = os.path.basename(j[3].strip())
                encoded_file = j[4].strip()
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send file {} from {} to group {}" . format(session_id, filename, sender, j[2].strip()))
                return self.send_group_file(session_id, sender, group_receiver, filename, encoded_file)
            
            # INBOX
            elif (command == 'inbox'):
                session_id = j[1].strip()
                username = self.sessions[session_id]['username']
                logging.warning("INBOX: {}" . format(session_id))
                return self.get_inbox(session_id, username)


            ## EXTERNAL SERVER ##
            # INITIALIZE
            elif (command == 'addrealm'):
                realm_id = j[1].strip()
                realm_address_to = j[2].strip()
                realm_port_to = int(j[3].strip())
                logging.warning("ADD: realm {} at ip address {} port {}" . format(realm_id, realm_address_to, realm_port_to))
                return self.add_realm(realm_id, realm_address_to, realm_port_to, data)
            elif (command == 'recvaddrealm'):
                realm_id = j[1].strip()
                realm_address_to = j[2].strip()
                realm_port_to = int(j[3].strip())
                return self.recv_add_realm(realm_id, realm_address_to, realm_port_to)
            elif (command == 'connectedrealm'):
                return self.get_connected_realm()
            
            # PRIVATE
            elif (command == 'sendprivaterealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                receiver = j[3].strip()
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w)
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send private message from {} to {} in realm {}" . format(session_id, sender, receiver, realm_id))
                return self.send_private_message_realm(session_id, realm_id, sender, receiver, message, data)
            elif (command == 'recvsendprivaterealm'):
                sender = j[1].strip()
                realm_id = j[2].strip()
                receiver = j[3].strip()
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w)
                logging.warning("RECV: receive private message from {} in realm {}" . format(sender, realm_id))
                return self.recv_private_message_realm(realm_id, sender, receiver, message)
            elif (command == 'sendprivatefilerealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                receiver = j[3].strip()
                filename = os.path.basename(j[4].strip())
                encoded_file = j[5].strip()
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send private file {} from {} to {} in realm {}" . format(session_id, filename, sender, receiver, realm_id))
                return self.send_private_file_realm(session_id, realm_id, sender, receiver, filename, encoded_file, data)
            elif (command == 'recvsendprivatefilerealm'):
                sender = j[1].strip()
                realm_id = j[2].strip()
                receiver = j[3].strip()
                filename = os.path.basename(j[4].strip())
                encoded_file = j[5].strip()
                logging.warning("RECV: receive private file {} from {} in realm {}".format(filename, sender, realm_id))
                return self.recv_private_file_realm(realm_id, sender, receiver, filename, encoded_file)
            
            # GROUP
            elif (command == 'sendgrouprealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                group_receiver = j[3].strip().split(',')
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w)
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send message from {} to group {} in realm {}".format(session_id, sender, group_receiver, realm_id))
                return self.send_group_message_realm(session_id, realm_id, sender, group_receiver, message, data)
            elif (command == 'recvsendgrouprealm'):
                sender = j[1].strip()
                realm_id = j[2].strip()
                group_receiver = j[3].strip().split(',')
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w) 
                logging.warning("RECV: receive message from {} in realm {}".format(sender, realm_id))
                return self.recv_group_message_realm(realm_id, sender, group_receiver, message)
            elif (command == 'sendgroupfilerealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                group_receiver = j[3].strip().split(',')
                filename = os.path.basename(j[4].strip())
                encoded_file = j[5].strip()
                sender = self.sessions[session_id]['username']
                logging.warning("SEND: session {} send file {} from {} to group {} in realm {}".format(session_id, filename, sender, group_receiver, realm_id))
                return self.send_group_file_realm(session_id, realm_id, sender, group_receiver, filename, encoded_file, data)
            elif (command == 'recvsendgroupfilerealm'):
                sender = j[1].strip()
                realm_id = j[2].strip()
                group_receiver = j[3].strip().split(',')
                filename = os.path.basename(j[4].strip())
                encoded_file = j[5].strip()
                logging.warning("RECV: receive file {} from {} in realm {}".format(filename, sender, realm_id))
                return self.recv_group_file_realm(realm_id, sender, group_receiver, filename, encoded_file)

            # INBOX
            elif (command == 'inboxrealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                username = self.sessions[session_id]['username']
                logging.warning("INBOX: {} in realm {}".format(session_id, realm_id))
                return self.inbox_realm(session_id, username, realm_id, data)
            elif (command == 'chatrealm'):
                session_id = j[1].strip()
                realm_id = j[2].strip()
                username = self.sessions[session_id]['username']
                logging.warning("INBOX: from realm {}".format(realm_id))
                return self.chat_realm(username, realm_id)
            
            
            ## INFO ##
            elif (command == 'logininfo'):
                return self.login_info()
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return { 'status': 'ERROR', 'message' : 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}


    ## UTIL ##
    def get_user(self, username):
        if (username not in self.users):
            return False
        return self.users[username]
    
    def login_info(self):
        if (len(self.sessions) != 0):
            return {'status': 'filled', 'message': self.sessions}
        return {'status': 'empty'}
        
    ## AUTH ##
    def login_user(self, username, password):
        if (username not in self.users):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        if (self.users[username]['password']!= password):
            return {'status': 'ERROR', 'message': 'Password Salah'}
        
        token_id = str(uuid.uuid4()) 
        self.sessions[token_id]={'username': username, 'user_detail': self.users[username]}
        return {'status': 'OK', 'token_id': token_id}
    
    def register_user(self, username, password, name, country):
        if (username in self.users):
            return {'status': 'ERROR', 'message': 'User Telah Terdaftar'}
        
        name = name.replace("_", " ")
        self.users[username]={ 
            'name': name,
            'country': country,
            'password': password,
            'incoming': {},
            'outgoing': {}
        }
        return {'status': 'OK', 'message': 'User Berhasil Didaftarkan'}

    def logout_user(self, session_id):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}

        del self.sessions[session_id]
        return {'status': 'OK', 'messages': 'User Berhasil Keluar'}
    
    
    ## INTERNAL SERVER ##
    # PRIVATE
    def send_private_message(self, session_id, sender, receiver, message):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}

        msg = {'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:	
            outqueue_sender[sender].put(msg)
        except KeyError:
            outqueue_sender[sender] = Queue()
            outqueue_sender[sender].put(msg)
        try:
            inqueue_receiver[sender].put(msg)
        except KeyError:
            inqueue_receiver[sender] = Queue()
            inqueue_receiver[sender].put(msg)
            
        return {'status': 'OK', 'message': 'Pesan Berhasil Dikirim'}
    
    def send_private_file(self, session_id, sender, receiver, filename ,encoded_file):
        if session_id not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}

        message = {
            'msg_from': s_fr['name'],
            'msg_to': s_to['name'],
            'file_name': filename,
            'file_content': encoded_file
        }
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[sender].put(json.dumps(message))
        except KeyError:
            outqueue_sender[sender] = Queue()
            outqueue_sender[sender].put(json.dumps(message))
        try:
            inqueue_receiver[sender].put(json.dumps(message))
        except KeyError:
            inqueue_receiver[sender] = Queue()
            inqueue_receiver[sender].put(json.dumps(message))
        
        child = f"{filename}_{sender}_{receiver}"
        folder = join(dirname(realpath(__file__)), '../BE/files/')
        os.makedirs(folder, exist_ok=True)
        folder = join(folder, child)
        os.makedirs(folder, exist_ok=True)
        file_location = os.path.join(folder, filename)
        if 'b' in encoded_file[0]:
            msg = encoded_file[2:-1]

            with open(file_location, "wb") as f:
                f.write(base64.b64decode(msg))
        else:
            encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Berhasil Dikirim'}
    
    # GROUP
    def send_group_message(self, session_id, sender, group_receiver, message):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(sender)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            msg = {'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message}
            outqueue_sender = s_fr['outgoing']
            inqueue_receiver = s_to['incoming']
            try:    
                outqueue_sender[sender].put(msg)
            except KeyError:
                outqueue_sender[sender] = Queue()
                outqueue_sender[sender].put(msg)
            try:
                inqueue_receiver[sender].put(msg)
            except KeyError:
                inqueue_receiver[sender] = Queue()
                inqueue_receiver[sender].put(msg)
                
        return {'status': 'OK', 'message': 'Pesan Grup Berhasil Dikirim'}
    
    def send_group_file(self, session_id, sender, group_receiver, filename, encoded_file):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(sender)
        if s_fr == False:
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}

        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            message = {
                'msg_from': s_fr['name'],
                'msg_to': s_to['name'],
                'file_name': filename,
                'file_content': encoded_file
            }
            outqueue_sender = s_fr['outgoing']
            inqueue_receiver = s_to['incoming']
            try:
                outqueue_sender[sender].put(json.dumps(message))
            except KeyError:
                outqueue_sender[sender] = Queue()
                outqueue_sender[sender].put(json.dumps(message))
            try:
                inqueue_receiver[sender].put(json.dumps(message))
            except KeyError:
                inqueue_receiver[sender] = Queue()
                inqueue_receiver[sender].put(json.dumps(message))
        
            child = f"{filename}_{sender}_{receiver}"
            folder = join(dirname(realpath(__file__)), '../BE/files/')
            os.makedirs(folder, exist_ok=True)
            folder = join(folder, child)
            os.makedirs(folder, exist_ok=True)
            file_location = os.path.join(folder, filename)
            if 'b' in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_location, "wb") as f:
                    f.write(base64.b64decode(msg))
            else:
                encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Grup Berhasil Dikirim'}
    
    # INBOX
    def get_inbox(self, session_id, username):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(username)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())
                
        return {'status': 'OK', 'messages': msgs}


    ## EXTERNAL SERVER ##
    # INITIALIZE
    def add_realm(self, realm_id, realm_address_to, realm_port_to, data):
        if realm_id in self.realms:
            return {'status': 'ERROR', 'message': 'Realm Telah Terdaftar'}

        self.realms[realm_id] = RealmBridge(self, realm_address_to, realm_port_to, self.users)
        
        j = data.split()
        j[0] = "recvaddrealm"
        data = ' '.join(j)
        data += "\r\n"
        
        return self.realms[realm_id].sendstring(data)

    def recv_add_realm(self, realm_id, realm_address_to, realm_port_to):
        self.realms[realm_id] = RealmBridge(self, realm_address_to, realm_port_to, self.users)
        return {'status':'OK', 'message': 'Realm Berhasil Dibuat'}

    def get_connected_realm(self):
        realms = {}
        for realm_id in self.realms:
            realms[realm_id] = [self.realms[realm_id].realm_address_to, self.realms[realm_id].realm_port_to, self.realms[realm_id].users]
            
        return { 'status': 'OK', 'messages': realms}

    # PRIVATE
    def send_private_message_realm(self, session_id, realm_id, sender, receiver, message, data):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        msg = { 'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message }
        self.realms[realm_id].put(msg)
        
        j = data.split()
        j[0] = "recvsendprivaterealm"
        j[1] = sender
        data = ' '.join(j)
        data += "\r\n"
        
        return self.realms[realm_id].sendstring(data)
    
    def recv_private_message_realm(self, realm_id, sender, receiver, message):
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar terima'}
        
        msg = { 'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message }
        self.realms[realm_id].put(msg)
        
        return {'status': 'OK', 'message': 'Pesan Berhasil Dikirim ke Realm'}
    
    def send_private_file_realm(self, session_id, realm_id, sender, receiver, filename, encoded_file, data):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        message = {
            'msg_from': s_fr['name'],
            'msg_to': s_to['name'],
            'file_name': filename,
            'file_content': encoded_file
        }
        self.realms[realm_id].put(message)
        
        child = f"{filename}_{sender}_{receiver}_{realm_id}"
        folder = join(dirname(realpath(__file__)), '../BE/files/')
        os.makedirs(folder, exist_ok=True)
        folder = join(folder, child)
        os.makedirs(folder, exist_ok=True)
        file_location = os.path.join(folder, filename)
        if 'b' in encoded_file[0]:
            msg = encoded_file[2:-1]

            with open(file_location, "wb") as f:
                f.write(base64.b64decode(msg))
        else:
            encoded_file.split()
        
        j = data.split()
        j[0] = "recvsendprivatefilerealm"
        j[1] = sender
        data = ' '.join(j)
        data += "\r\n"
        return self.realms[realm_id].sendstring(data)
    
    def recv_private_file_realm(self, realm_id, sender, receiver, filename, encoded_file):
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        s_to = self.get_user(receiver)
        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        message = {
            'msg_from': s_fr['name'],
            'msg_to': s_to['name'],
            'file_name': filename,
            'file_content': encoded_file
        }
        self.realms[realm_id].put(message)
        
        child = f"{filename}_{sender}_{receiver}_{realm_id}"
        folder = join(dirname(realpath(__file__)), '../BE/files/')
        os.makedirs(folder, exist_ok=True)
        folder = join(folder, child)
        os.makedirs(folder, exist_ok=True)
        file_location = os.path.join(folder, filename)
        if 'b' in encoded_file[0]:
            msg = encoded_file[2:-1]

            with open(file_location, "wb") as f:
                f.write(base64.b64decode(msg))
        else:
            encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Berhasil Dikirim ke Realm'}

    # GROUP
    def send_group_message_realm(self, session_id, realm_id, sender, group_receiver, message, data):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if realm_id not in self.realms:
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            msg = {'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message }
            self.realms[realm_id].put(msg)
        
        j = data.split()
        j[0] = "recvsendgrouprealm"
        j[1] = sender
        data = ' '.join(j)
        data +="\r\n"
        return self.realms[realm_id].sendstring(data)
    
    def recv_group_message_realm(self, realm_id, sender, group_receiver, message):
        if realm_id not in self.realms:
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
        
        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            msg = {'msg_from': s_fr['name'], 'msg_to': s_to['name'], 'msg': message }
            self.realms[realm_id].put(msg)
            
        return {'status': 'OK', 'message': 'Pesan Grup Berhasil Dikirim ke Realm'}
    
    def send_group_file_realm(self, session_id, realm_id, sender, group_receiver, filename, encoded_file, data):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        if (s_fr == False):
                return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
            
        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            message = {
                'msg_from': s_fr['name'],
                'msg_to': s_to['name'],
                'file_name': filename,
                'file_content': encoded_file
            }
            self.realms[realm_id].put(message)
        
            child = f"{filename}_{sender}_{receiver}_{realm_id}"
            folder = join(dirname(realpath(__file__)), '../BE/files/')
            os.makedirs(folder, exist_ok=True)
            folder = join(folder, child)
            os.makedirs(folder, exist_ok=True)
            file_location = os.path.join(folder, filename)
            if 'b' in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_location, "wb") as f:
                    f.write(base64.b64decode(msg))
            else:
                encoded_file.split()
        
        j = data.split()
        j[0] = "recvsendgroupfilerealm"
        j[1] = sender
        data = ' '.join(j)
        data += "\r\n"
        return self.realms[realm_id].sendstring(data)

    def recv_group_file_realm(self, realm_id, sender, group_receiver, filename, encoded_file):
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(sender)
        if (s_fr == False):
                return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
            
        for receiver in group_receiver:
            s_to = self.get_user(receiver)
            if s_to is False:
                continue
            
            message = {
                'msg_from': s_fr['name'],
                'msg_to': s_to['name'],
                'file_name': filename,
                'file_content': encoded_file
            }
            self.realms[realm_id].put(message)
        
            child = f"{filename}_{sender}_{receiver}_{realm_id}"
            folder = join(dirname(realpath(__file__)), '../BE/files/')
            os.makedirs(folder, exist_ok=True)
            folder = join(folder, child)
            os.makedirs(folder, exist_ok=True)
            file_location = os.path.join(folder, filename)
            if 'b' in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_location, "wb") as f:
                    f.write(base64.b64decode(msg))
            else:
                encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Grup Berhasil Dikirim ke Realm'}
    
    # INBOX
    def inbox_realm(self, session_id, username, realm_id, data):
        if (session_id not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(username)
        if (s_fr == False):
                return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
            
        j = data.split()
        j[0] = "chatrealm"
        data = ' '.join(j)
        data += "\r\n"
        return self.realms[realm_id].sendstring(data)
    
    def chat_realm(self, username, realm_id):
        if (realm_id not in self.realms):
            return {'status': 'ERROR', 'message': 'Realm Tidak Terdaftar'}
        
        s_fr = self.get_user(username)
        if (s_fr == False):
            return {'status': 'ERROR', 'message': 'User Tidak Terdaftar'}
            
        msgs = []
        while not self.realms[realm_id].chats[s_fr['name']].empty():
            msgs.append(self.realms[realm_id].chats[s_fr['name']].get_nowait())
            
        return {'status': 'OK', 'messages': msgs}

if __name__=="__main__":
    j = Chat()
    sesi = j.proses("auth messi surabaya")
    print(sesi)
    sesi2 = j.proses("auth henderson surabaya")
    token_id = sesi['token_id']
    # token_id2 = sesi2['token_id']
    print(j.proses("send {} henderson hello gimana kabarnya son " . format(token_id)))
    # print(j.proses("send {} messi hello gimana kabarnya mess " . format(token_id)))

    #print j.send_message(token_id,'messi','henderson','hello son')
    #print j.send_message(token_id,'henderson','messi','hello si')
    #print j.send_message(token_id,'lineker','messi','hello si dari lineker')


    # print("isi mailbox dari messi")
    # print(j.get_inbox('messi'))
    print("isi mailbox dari henderson")
    print(j.get_inbox('henderson'))