# найти ошибку, почему сайт не работает !!!

import random
import nltk
import json
import logging
import sklearn
from telegram import ParseMode
import telebot
import logging
import datetime
import requests
from pprint import pprint
from telegram import Update, ForceReply, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

# открытие словаря
try:
    with open("Data_Base.json", "r", encoding="utf-8") as file:
        BOT_CONFIG = json.load(file)
except:
    print("WARNING")

print("Successfully")

        # Приветствие ( /start )
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text(fr'{user.mention_markdown_v2()}\!')

        # Остальные сообщения
corpus = []
y = []
for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'][intent]['examples']:
        corpus.append(example)
        y.append(intent)

corpus_train, corpus_test, y_train, y_test = sklearn.model_selection.train_test_split(corpus, y, test_size=0.2)
# векторайзер
# vectorizer = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(2,4), analyzer='char_wb')
vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(ngram_range=(2, 4), analyzer='char_wb', use_idf=True)
X_train = vectorizer.fit_transform(corpus_train)
X_test = vectorizer.transform(corpus_test)
clf = sklearn.linear_model.RidgeClassifier(copy_X=True, max_iter=200)
# clf = sklearn.ensemble.RandomForestClassifier()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)

    # подписка к векторайзеру
def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]

def bot(text):
  intent = get_intent_by_model(text)
  if intent != 'intent not found:(':
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])
  else:
    return 'Некорректная форма вопроса!'

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    input_text = update.message.text
    reply = bot(input_text)
    update.message.reply_text(reply)

# Главная функция
def main() -> None:
    print("MAIN")

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Телеграмм токен
    updater = Updater("5061820313:AAFPQ26ELLjfYFDJmfHNFEIUG14svbc4Wyw")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
# СЛЕШОВЫЕ команды
  
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
  # Цикл,который никогда не закончится,пока его не отстановишь
    updater.idle()

if __name__ == '__main__':
    main()