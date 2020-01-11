import json
import logging

from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class Notifier:
    def __init__(self, name, greeting, token):
        self.logger = logging.getLogger(__name__)
        self.name=name
        self.greeting = greeting

        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        self.updater.start_polling()

        self.registered = []
        self.logger.info(f'started notifier for {self.name}')

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,text=self.greeting)
        self.registered.append((context, update))
        self.logger.info(f'registered {update.effective_chat.id}')

    def send_notification(self, message):
        for context, update in self.registered:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            self.logger.info(f'sent notification to {update.effective_chat.id}: {message}')


if __name__ == '__main__':
    import pathlib
    import time

    config = json.loads(pathlib.Path('config-notifier.json').read_text())
    notifier = Notifier(name=config['name'], greeting=config['greeting'], token=config['token'])

    while True:
        notifier.send_notification('Test')
        time.sleep(5)
