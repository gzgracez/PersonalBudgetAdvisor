from ask import alexa
import urllib2
import json
#import sqlite3
import helpers

# connect SQLite 
# account = sqlite3.connect("account.db")
# cursor = account.cursor()

def lambda_handler(request_obj, context={}):
    return alexa.route_request(request_obj)

@alexa.default_handler()
def default_handler(request):
    return launch_request_handler(request)

@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Hello! I am here to be your account manager. What would you like to know?",
                                 reprompt_message='You can ask about your bank account and I will tell you!')

@alexa.request_handler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Be wise in your spending today! Goodbye.", end_session=True)

@alexa.intent_handler("GetCurrentBalance")
def get_current_balance_handler(request):
    #net balance
    net_balance = helpers.getTotalBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Your current net balance is ${}".format(str(net_balance))
    #conditionals if balance does not exist
    if net_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)

@alexa.intent_handler("GetCreditBalance")
def get_credit_balance_handler(request):
    #retrieve current balance of the credit card
    credit_balance = helpers.getCreditCardBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Credit card current balance is ${}".format(str(credit_balance))
    #conditionals if balance does not exist
    if credit_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)

@alexa.intent_handler("GetCheckingBalance")
def get_checking_balance_handler(request):
    #retrieve current balance of the checking account
    checking_balance = helpers.getCheckingBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Checking account current balance is ${}".format(str(checking_balance))
    #conditionals if balance does not exist
    if checking_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)


@alexa.intent_handler("GiveSuggestions")
def give_suggestions_handler(request):
    #retrieve what category the user wanted
    category = str(request.get_slot_value("category")).lower()
    #start with empty string
    message = ""
    #if the user didn't provide category, tell it to try again
    if category == "":
        message = message + "Please try again and specify the category you are looking for."
        boolEndValue = False
    #when the user did provide category, follow through
    else:
        if category == "shopping":
            value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "store", 3)
            message = message + "For {}, you should spend ${}.".format(category, value)
            boolEndValue = True
        elif category == "food":
            value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", category, 3)
            message = message + "For {}, you should spend ${}.".format(category, value)
            boolEndValue = True
        elif category == "gas":
            value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "food", 3)
            message = message + "For {}, you should spend ${}.".format(category, value)
            boolEndValue = True
        elif category == "shopping":
            value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", category, 3)
            message = message + "For {}, you should spend ${}.".format(category, value)
            boolEndValue = True
        elif category == "clothes":
            value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", category, 3)
            message = message + "For {}, you should spend ${}.".format(category, value)
            boolEndValue = True
        else:
            message = message + "Sorry, we don't have information about that. Try a different category."
            boolEndValue = False

    return alexa.create_response(message=message, end_session=boolEndValue)


@alexa.intent_handler("AMAZON.HelpIntent")
def help_intent_handler(request):
    return alexa.create_response(message="This skill gives information about your bank account.", end_session=False)

@alexa.intent_handler("AMAZON.StopIntent")
def stop_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)

@alexa.intent_handler("AMAZON.CancelIntent")
def cancel_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)
