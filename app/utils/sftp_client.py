import paramiko
import os

def upload_file_sftp(local_path, host, port, username, password, remote_dir):
    transport = None
    sftp = None

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        filename = os.path.basename(local_path)
        remote_path = f"{remote_dir}/{filename}"

        sftp.put(local_path, remote_path)

        print(f"SFTP 업로드 성공: {remote_path}")

    except Exception as e:
        raise RuntimeError(f"SFTP 전송 실패: {e}")

    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()