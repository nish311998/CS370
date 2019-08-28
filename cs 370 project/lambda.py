import random
import pandas as pd
import datetime
CardTitlePrefix = "Traintime"
# --------------- Load Data ------------------

stop_time_data = pd.read_csv('./CS370data/stop_times.txt', sep=",", header=None)
stop_time_data.columns = ["trip_id", "arrival_time" , "departure_time" , "stop_id" ," stop_sequence" ,"pickup_type" ,"drop_off_type", "shape_dist_traveled"]

stops_data = pd.read_csv('./CS370data/stops.txt', sep=",", header=None)
stops_data.columns = ["stop_id","stop_code","stop_name","stop_desc","stop_lat","stop_lon","zone_id"]

trips_data = pd.read_csv('./CS370data/trips.txt', sep=",", header=None)
trips_data.columns = ["route_id","service_id","trip_id","trip_headsign","direction_id","block_id","shape_id"]



# --------------- Train Fncs ------------------

def get_dest_info(starting, ending, direction):
    for (idx,row) in stops_data.iterrows():
        if row.loc['stop_name'] == starting.upper():#determining if we have data for the inputs
            val = get_times(row.loc["stop_id"], direction)
            return val

def get_times(stop_id, direction):
    train_times = []
    for (idx,row) in stop_time_data.iterrows():
        if row.loc['stop_id'] == stop_id:
            if direction.lower() == 'north':
                direction = 0
            else:
                direction = 1
            val = get_trips(row.loc['trip_id'], direction)
            now = datetime.datetime.now()#might have to check if time is greater than hour 24
            if row.loc["arrival_time"] < "23:59:59":
                if val == 1 and pd.to_datetime(row.loc["arrival_time"])>now:
                    train_times.append(row.loc["arrival_time"])
    return train_times


def get_trips(trip_id, direction):
    for (idx,row) in trips_data.iterrows():
        if row.loc['trip_id'] == trip_id:
            if direction == row.loc['direction_id']:
                return 1
            else:
                return 0


# --------------- Main handler ------------------

def lambda_handler(event, context):
   
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
        

# --------------- Helpers that build all of the responses in JSON Format----------------------

def build_s_response(title, output, reprompt_text, should_end_session):
  

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
 
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_w_response():
    session_attributes = {}
    card_title = "Hello"
    speech_output = "Ask me your starting station and ending station"
    reprompt_text = "You should ask me about your train information"
    should_end_session = False
    return build_response(session_attributes, build_s_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you and have a nice day!"
    should_end_session = True
    return build_response({}, build_s_response(card_title, speech_output, None, should_end_session))

def get_info(fromStation, endStation, direction):#edit this method
   
    card_title = "Train Info Result"
    #call our outside function here and retrun it into build response
    lst=[]
    lst = get_dest_info(fromStation, endStation, direction)
    lst=list(set(lst))
    lst.sort()
    outputstring = ','.join(lst)
    return build_response({}, build_s_response(card_title, outputstring, "You should ask me about your train information", True))

# --------------- Events ------------------

def on_session_started(session_started_request, session):

    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_w_response()


def on_intent(intent_request, session):

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "GetInfo":
        fromStation=intent_request['intent']['slots']['fromStation']['value']
        endStation=intent_request['intent']['slots']['endStation']['value']
        direction=intent_request['intent']['slots']['direction']['value']
        return get_info(fromStation,endStation,direction)
    elif intent_name == "AMAZON.HelpIntent":
        return get_w_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

