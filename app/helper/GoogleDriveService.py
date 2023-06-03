from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def createService():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    return drive

def uploadFile(drive, title):
    folder = "1GJSHcpFRccxgFyW6ziIgPvDTbUR2e3qL"

    file1 = drive.CreateFile({
        'parents': [{'id': folder}],
        'title': title
    })

    path = "./app/temp/"+title
    file1.SetContentFile(path)
    file1.Upload()

    file1.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    return file1['id']