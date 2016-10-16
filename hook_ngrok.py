import telepot
import requests
import os
import time
from multiprocessing import Process

token = '294289451:AAEjcnW1o4b4zsJTGI9MG46z4cock-sWC_M'
port = 8000
wait_time = 3  # seconds


def ngrok_callback():
    print('[*] Starting ngork')
    os.system('ngrok start --all'.format(port))


def hook_callback(bot):
    print('[*] Requesting public tunnels')
    data = requests.get('http://localhost:4040/api/tunnels')
    print('[*] Searching https tunnel')
    for t in data.json()['tunnels']:
        if t['proto'] == 'https':
            tunnel = t['public_url']
            break
    else:
        raise RuntimeError('No https tunnel')
    print('[*] Hooking on public tunnel: {}'.format(tunnel))

    url = '{}/sheds/bot/{}'.format(tunnel, token)

    if bot.setWebhook(url):
        print('[+] Hooked!')
    else:
        print('[-] failure :c')
        raise RuntimeError('Not hooked')


def main():
    print('[*] Loading bot')
    bot = telepot.Bot(token)

    if bot:
        print('[+] Bot: OK')
        for k, v in bot.getMe().items():
            print('[*] {}: {}'.format(k, v))
    else:
        raise RuntimeError('Bot not found')

    ngrok_worker = Process(target=ngrok_callback)
    ngrok_worker.start()

    integrator = Process(target=time.sleep, args=(wait_time,))
    print('[*] Waining for {} seconds...'.format(wait_time))
    integrator.start()
    integrator.join()

    hook_worker = Process(target=hook_callback, args=(bot,))
    hook_worker.start()
    hook_worker.join()

    ngrok_worker.join()

if __name__ == '__main__':
    main()
