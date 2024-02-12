from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import keys
import random
import csv

TOKEN: Final = keys.Bot_Token
BOT_USERNAME: Final = keys.Bot_Username

insultTargets = {
    'mark' : 'Markryann',
    'chris' : 'Chrisdouglass',
    'keagan' : 'keaganoliverio',
    'maj' : 'majells',
    'fel' : 'feliciachiam',
    'deion' : 'Deionos',
    'skye' : 'schuylerholland',
    'james' : 'Pereira_James'
}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('WAS UP FKER!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I HELP!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('CUSTUMMM')

# Responses
def generate_Insult(targetsUsername):

    flipped_dict = {value: key for key, value in insultTargets.items()}

    targetName = flipped_dict[targetsUsername]

    filename = 'insultTargets/' + targetName + '.csv'

    targetInsults = []

    with open(filename) as file:
        file_data = csv.reader(file,delimiter=',')
        # next(file_data) #skips the header
        for row in file_data:
            tempList = []
            tempList.append(row[0])
            tempList.append(int(row[1]))
            targetInsults.append(tempList)

    insult = ""

    while insult == "":
        All_Count = 1
        for i in range(1, len(targetInsults)):
            if targetInsults[i][1] == targetInsults[0][1]:
                All_Count += 1

        if All_Count == len(targetInsults):
            targetInsults[0][1] += 1

        ranNum = random.randint(1,len(targetInsults)- 1)
        if targetInsults[ranNum][1] < targetInsults[0][1]:
            insult = targetInsults[ranNum][0]
            targetInsults[ranNum][1] += 1

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(targetInsults)

    return insult

def handle_response(text: str) -> str:
    proceseed: str = text.lower()

    if "dong" in proceseed:
        return "Did you just say dong"
    if "dick" in proceseed:
        return "GAYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYEHHHHHHHHHHHHHHH"
        

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.message.chat.username

    # location_long = update.message.location.latitude
    # location_lat = update.message.location.longitude

    message_type: str = update.message.chat.type

    if message_type != "private":
        message_type = update.message.chat.title

    text: str = update.message.text

    targetsName = update.message.from_user.username

    print(f'{targetsName} ({update.message.chat.id}) in {message_type}: "{text}"')

    # print(location_lat)
    # print(location_long)

    for i in insultTargets:
        if targetsName == insultTargets[i]:
            ranNum = random.randint(0,1)
            print("Random Number: " + str(ranNum))
            if ranNum == 1:
                insult = generate_Insult(targetsName)
                print("JasonBot: " + insult)
                await update.message.reply_text(insult)

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
       

    if response != None:
        print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Can be used to get user information
    # print(f'Update {update} caused error {context.error}')
    return

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    app.run_polling(poll_interval=1)