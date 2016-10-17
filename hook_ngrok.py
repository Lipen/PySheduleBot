import telepot
import requests
import os
import time
import traceback
from multiprocessing import Process, Pipe, Queue

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


def bot_callback(queue):
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
        s = '[*] Bot info:'
        for k, v in bot.getMe().items():
            s += '\n -  {}: {}'.format(k, v)
        print(s)
    else:
        print('[-] Bot: FAIL')
        raise BotError

    print('[*] Waiting for public tunnel')
    tunnel = queue.get()
    url = '{}/sheds/bot/{}'.format(tunnel, token)

    print('[*] Hooking')
    if bot.setWebhook(url):
        print('[+] Hooked!')
    else:
        print('[-] Hook: FAIL')
        raise WebhookError


def ngrok_callback():
    print('[*] Starting ngork')
    os.system('ngrok start base --config ngrok.yml'.format(port))
    # os.system('bash -c "while true; do true; done"')


def tunnel_callback(queue):
    print('[*] Requesting public tunnels')
    data = requests.get('http://localhost:4040/api/tunnels')

    print('[*] Searching https tunnel')
    for t in data.json()['tunnels']:
        if t['proto'] == 'https':
            tunnel = t['public_url']
            break
    else:
        raise NoTunnelError

    print('[*] Found public https tunnel: {}'.format(tunnel))
    queue.put(tunnel)

def hatiko_callback(wait_time):
    print('[*] Hatiko: awaits {} seconds...'.format(wait_time))
    time.sleep(wait_time)


def main():
    queue = Queue()

    bot_worker = ProcessEx(target=bot_callback, args=(queue,))
    bot_worker.start()

    ngrok_worker = Process(target=ngrok_callback)
    ngrok_worker.start()

    while 1:
        hatiko = Process(target=hatiko_callback, args=(wait_time,))
        hatiko.start()
        hatiko.join()

        tunnel_worker = ProcessEx(target=tunnel_callback, args=(queue,))
        tunnel_worker.start()
        tunnel_worker.join()

        ex = tunnel_worker.exception
        if ex:
            e, tb = ex  # (exception, traceback)
            if isinstance(e, NoTunnelError):
                print('[!] Hook: retrying')
                continue
            else:
                raise e
        else:
            break

    bot_worker.join()
    ex = bot_worker.exception
    if ex:
        e, tb = ex
        raise e

    print('[+] Running hooked ngrok ...')
    ngrok_worker.join()

if __name__ == '__main__':
    main()
