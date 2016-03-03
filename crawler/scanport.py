import socket as S
def scan(ip, arg):
        result = []
        if arg == '*': portas = range(1,65536)
        elif '-' in arg:
                arg = arg.split('-')
                portas = range(int(arg[0]), int(arg[1])+1)
                
        else: portas = [int(arg)]
        
        socket = S.socket(S.AF_INET, S.SOCK_STREAM)
        def analisa(ip, port):
                try:
                        socket.connect((ip, port))
                        return True
                except:
                        return False
        for port in portas:
                resposta = analisa(ip, int(port))
                if resposta == True:
                        x = 'porta {port} ABERTA em {ip}'.format(port = port, ip = ip)
                        result.append(x)
                else:
                        bad = 'porta {port} FECHADA em {ip}'.format(port = port, ip = ip)
                        result.append(bad)
        ans = ""
        for i in result:
                ans += "{}\n".format(i)
        return ans