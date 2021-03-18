from PySock.PySock import commModule

def test_FormatIPEXT():
    comm = commModule('192.168.1.1:80')

    assert comm.IP == '192.168.1.1'
    assert comm.PORT == '80'

def test_FormatIPPORT():
    comm = commModule('192.168.1.1', '80')

    assert comm.IP == '192.168.1.1'
    assert comm.PORT == '80'

def test_Set():
    comm = commModule('192.168.1.1:80')

    comm.PORT = '20'

    assert comm.PORT == '20'
