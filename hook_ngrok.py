import telepot
import requests
import os
import time
import traceback
from multiprocessing import Process, Pipe

port = 8000
wait_time = 3  # seconds


class ProcessEx(Process):

    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):
        try:
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still raise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


class NoTunnelError(RuntimeError):
    pass


class WebhookError(RuntimeError):
    pass


class TokenError(RuntimeError):
    pass


class BotError(RuntimeError):
    pass


def ngrok_callback():
    print('[*] Starting ngork')
    os.system('ngrok start base --config ngrok.yml'.format(port))


def hook_callback(bot, token):
    print('[*] Requesting public tunnels')
    data = requests.get('http://localhost:4040/api/tunnels')
    print('[*] Searching https tunnel')
    for t in data.json()['tunnels']:
        if t['proto'] == 'https':
            tunnel = t['public_url']
            break
    else:
        raise NoTunnelError
    print('[*] Hooking on public tunnel: {}'.format(tunnel))

    url = '{}/sheds/bot/{}'.format(tunnel, token)

    if bot.setWebhook(url):
        print('[+] Hooked!')
    else:
        print('[-] failure :c')
        raise WebhookError


def main():
    print('[*] Loading token')
    try:
        with open('token') as f:
            token = f.read().strip()
        if not token:
            raise TokenError
    except:
        print('[-] Token: FAIL')
        raise TokenError
    else:
        print('[+] Token: OK')

    print('[*] Loading bot')
    bot = telepot.Bot(token)

    if bot:
        print('[+] Bot: OK')
        for k, v in bot.getMe().items():
            print('\t[*] {}: {}'.format(k, v))
    else:
        print('[-] Bot: FAIL')
        raise BotError

    ngrok_worker = Process(target=ngrok_callback)
    ngrok_worker.start()

    while 1:
        hatiko = Process(target=time.sleep, args=(wait_time,))
        print('[*] Waining for {} seconds...'.format(wait_time))
        hatiko.start()
        hatiko.join()

        hook_worker = ProcessEx(target=hook_callback, args=(bot, token))
        hook_worker.start()
        hook_worker.join()

        e_tb = hook_worker.exception
        if e_tb:
            e, tb = e_tb
            if isinstance(e, NoTunnelError):
                print('[!] Retrying to hook')
            else:
                raise e
        else:
            break

    print('[+] Running hooked ngrok ...')
    ngrok_worker.join()

if __name__ == '__main__':
    main()
