from win32clipboard import OpenClipboard, GetClipboardData
from string import printable

def get_clip():
    OpenClipboard()
    data = ''.join([s if s in printable else '' for s in GetClipboardData()])
    return data
    
if __name__ == '__main__':
    print(get_clip())
