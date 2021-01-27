# -*- coding: UTF-8 -*-
# Public package
# Private package
import paramiko


def upload(host, user, password, local_path, server_path, timeout=10):
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False


def download(host, user, password, server_path, local_path, timeout=10):
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False
