
import sys
import csv
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import os
import pyaudio
# speech recognition framework
from vosk import Model, KaldiRecognizer
import pyttsx3
import json
import winsound
from datetime import datetime
import time
import speech_recognition as sr
from pydub import AudioSegment

msg1_welcome = "Welcome to Demo bank. How can we help you Today?"
msg2_good_bye = "Thank you for Banking with us."
msg3_customer_identify1 = "Sure, Let us help you. Please confirm your identity."
msg4_customer_identify_name = "State your full name."
msg5_unable_to_understand_voice_input = "Unable to understand the statement.. Please try again"
msg6_exiting = "\n\nDisconnecting now..."
msg7_empty = ""
msg8_exit = "Exit"
msg9_customer_identify_OTP = "Tell your 4 digit OTP ot TPIN."
msg10_customer_name_identity_done = "Your are a valid customer."
msg11_customer_name_identity_failed = "Invalid user name."
msg12_customer_OTP_done = "OTP validation done."
msg13_customer_OTP_failed = "OTP validation failed."
msg14_customer_overall_verification_failed = "Customer identity and OTP verification failed."
msg15_overall_concern = "Please briefly outline your concerns."
msg16_unsupported_task = "Unsupported task!"
msg17_guardrails_breached = "Guardrails breached!"
msg18_all_processing_done = "All processing Done!"



starting_timestamp = time.time()
attempt_count = 3
# need to wait min 3 sec for this app to init
listening_duration_min = 3
listening_duration = listening_duration_min + 4
known_customers = ["Jack Black", "Lisa Bush", "Victor Hugo"]
known_OTPs = ["one two three four", "four three two one"]
skip_welcome=False
skip_cust_name_check=False
skip_cust_OTP_check=False
ollama_cloud_model="gpt-oss:120b-cloud"
sentence_tx_model="all-MiniLM-L6-v2"
file_ollama_key = "ollama_api_key_file.txt"
file_prompt_guardrail = "prompt0_query_guardrails.txt"
file_prompt_sentiment = "prompt1_query_sentiment.txt"
unsupported_task_intent = "UNSUPPORTED_TASK"
guardrails_breach = "GUARDRAILS_BREACH"

# category wise supported tasks or services
Check_Account_Balance = ["CHECK_SAVINGS_BALANCE","CHECK_CURRENT_BALANCE","CHECK_OVERDRAFT_LIMIT","CHECK_UNCLEARED_FUNDS"]
Review_Recent_Transactions = ["GET_LAST_5_TRANSACTIONS","SEARCH_TRANSACTION_BY_DATE","SEARCH_TRANSACTION_BY_AMOUNT","CHECK_LAST_DEPOSIT"]
Transfer_Money = ["TRANSFER_INTERNAL", "TRANSFER_THIRD_PARTY", "SCHEDULE_RECURRING_TRANSFER", "MANAGE_BENEFICIARIES", "FUND_TRANSFER"]
Pay_Bills = ["PAY_CREDIT_CARD_BILL","PAY_UTILITY_BILL","RECHARGE_MOBILE_DTH","MANAGE_BILLERS"]
Report_Lost_or_Stolen_Card = ["BLOCK_CARD_PERMANENTLY","FREEZE_CARD_TEMPORARILY","BLOCK_INTERNET_BANKING"]
Activate_New_Card = ["GENERATE_ATM_PIN", "ACTIVATE_ONLINE_USAGE","ACTIVATE_INTERNATIONAL_USAGE", "UNFREEZE_CARD"]
Request_Account_Statement = ["EMAIL_MONTHLY_STATEMENT", "POST_PHYSICAL_STATEMENT", "GET_MINI_STATEMENT", "REQUEST_FINANCIAL_YEAR_STATEMENT"]
Check_Loan_Status = ["CHECK_APPLICATION_STATUS", "CHECK_OUTSTANDING_BALANCE", "CHECK_NEXT_EMI","REQUEST_FORECLOSURE_LETTER"]
Stop_Cheque_Payment = ["STOP_SINGLE_CHEQUE","STOP_CHEQUE_RANGE","CHECK_STOP_STATUS"]
Order_New_Cheque_Book = ["REQUEST_NEW_BOOK", "TRACK_CHEQUE_BOOK","CHANGE_DELIVERY_ADDRESS"]
Update_Contact_Information = ["UPDATE_MOBILE_NUMBER","UPDATE_EMAIL_ID","UPDATE_MAILING_ADDRESS","UPDATE_PAN_AADHAAR"]
Check_Credit_Card_Limit_n_Rewards = ["CHECK_AVAILABLE_LIMIT","CHECK_TOTAL_LIMIT","CHECK_REWARD_POINTS","REDEEM_POINTS"]
Dispute_a_Transaction = ["REPORT_FRAUD_TRANSACTION","DISPUTE_DOUBLE_DEBIT","DISPUTE_ATM_FAILURE", "CHECK_DISPUTE_STATUS"]
Find_Nearest_Branch_or_ATM = ["LOCATE_NEAREST_ATM","LOCATE_NEAREST_BRANCH","LOCATE_CASH_DEPOSIT_MACHINE","CHECK_BRANCH_HOURS"]
Check_Current_Interest_Rates = ["CHECK_FD_RATES","CHECK_SAVINGS_RATES","CHECK_HOME_LOAN_RATES","CHECK_SENIOR_CITIZEN_RATES"]
Get_Currency_Exchange_Rates = ["CHECK_BUYING_RATE", "CHECK_SELLING_RATE","CONVERT_CURRENCY"]
Open_Fixed_or_Recurring_Deposit = ["OPEN_FIXED_DEPOSIT", "OPEN_RECURRING_DEPOSIT", "PREMATURE_CLOSURE","RENEW_DEPOSIT"]
Request_Tax_Certificates = ["GET_TDS_CERTIFICATE", "GET_LOAN_INTEREST_CERT", "GET_DEPOSIT_INTEREST_CERT"]
Schedule_Branch_Appointment = ["BOOK_LOCKER_ACCESS", "MEET_LOAN_OFFICER", "KYC_APPOINTMENT", "RESCHEDULE_APPOINTMENT"]
Speak_to_Customer_Support_Agent = ["CONNECT_GENERAL_SUPPORT","CONNECT_LOAN_DEPT","CONNECT_FRAUD_DEPT","CONNECT_PRIORITY_DESK"]

all_audio_path = "C:\\Users\\malas\\shri_1000_names\\PythonProjects\\p18_ollama_IVRS1\\sound_sample_banking_with_disturbance\\"

# The multiple values you want to dump in csv
overall_result_file = 'overall_ivrs_' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.csv'
# Open the file in append mode ('a') with newline='' to prevent extra blank rows
my_csv = open(overall_result_file, mode='a', newline='')
writer_csv = csv.writer(my_csv)
writer_csv.writerow(["index", "Extracted text", "Guardrail Status", "Sentiment Status", "Valid Intent"])


def load_vosk_model():
    # model_path = "models/vosk-model-small-en-us"
    model_path = "models/vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Vosk model not found! Download and place it in the 'models' directory.")
    return Model(model_path)

def exit_ivrs():
    ai_bot_speak_this(msg6_exiting)
    winsound.MessageBeep()
    sys.exit()

def listen_to_customer_and_transcribe(model):
    global starting_timestamp
    global attempt_count
    global listening_duration
    # Vosk model and a sample rate of 16000 Hz
    ivrs_rec = KaldiRecognizer(model, 16000)
    # Initializes the PyAudio instance for handling audio input/output.
    ivrs_audio = pyaudio.PyAudio()
    ivrs_stream = ivrs_audio.open(
        # Opens an audio input stream
        format=pyaudio.paInt16,
        # Indicates mono audio (single channel)
        channels=1,
        # sample rate
        rate=16000,
        # Specifies that this stream is for audio input.
        input=True,
        # Sets the size of the buffer that holds audio data before being processed.
        frames_per_buffer=8192
        )
    ivrs_stream.start_stream()  # Begins the audio stream

    print("Listening... Speak now.")
    customer_said = ""
    attempt = False
    for n in range(attempt_count):
        try:
            while True:
                ivrs_data = ivrs_stream.read(num_frames=4096, exception_on_overflow=False)
                # Processes the audio chunk Returns True if the audio chunk is sufficient
                if ivrs_rec.AcceptWaveform(ivrs_data):
                    # Retrieves the transcription result as a JSON string
                    result = ivrs_rec.Result()
                    # Converts the JSON string into a Python dictionary
                    text = eval(result).get('text', '')
                    # exit after 10 words
                    # print("Customer said text length:" + str(len(text)))
                    # print("Customer said text:       " + text)
                    condition1_input_text = False
                    condition2_attempt_counter = False
                    condition3_exit_word = False
                    condition4_time_up = False

                    if len(text) > 10:
                        condition1_input_text = True
                    if n == 2:
                        condition2_attempt_counter = True
                    if text.lower() == msg8_exit.lower():
                        condition3_exit_word = True
                    current_ts = time.time()
                    # print(current_ts)
                    # print(starting_timestamp)
                    # print(current_ts - starting_timestamp)
                    if (current_ts + listening_duration) > starting_timestamp:
                        condition4_time_up = True

                    if (condition1_input_text or condition2_attempt_counter or
                            condition3_exit_word or condition4_time_up):
                        customer_said = text
                        attempt = True
                        break
        except Exception as e:
            print(e)
            print(msg5_unable_to_understand_voice_input)
            ai_bot_speak_this(msg5_unable_to_understand_voice_input)
            if n==2:
                attempt = True
        if attempt:
            break

    ivrs_stream.close()
    print(f"Customer said: ==>{customer_said}" + "<==")
    if customer_said.lower() in [msg8_exit.lower(), msg7_empty]:
        print(msg6_exiting)
        exit_ivrs()

    return customer_said

def ai_bot_speak_this(text):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def chunk_text(text: str, max_chunk_length: int = 2500) -> list:
    """
    Split text into smaller chunks; for RAG, shorter chunks are easier to retrieve.
    """
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 > max_chunk_length:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
        else:
            current_chunk += para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def embed_chunks(chunks: list, embedder) -> np.ndarray:
    """
    Compute embedding for each chunk.
    """
    return np.array([embedder.encode(chunk) for chunk in chunks])

def retrieve_relevant_chunks(query: str, chunks: list, chunk_embeddings: np.ndarray,
                              embedder, top_k: int = 3) -> list:
    """
    Retrieve top_k chunks that are most similar to the query.
    """
    query_embedding = embedder.encode(query)
    norms = np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
    similarities = np.dot(chunk_embeddings, query_embedding) / (norms + 1e-10)
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

def rag_summarize(document_text: str, query: str) -> str:
    """
    Given a document and a query, retrieve top relevant chunks and use them to prompt the LLM.
    """
    chunks = chunk_text(document_text)
    embedder = SentenceTransformer(sentence_tx_model)
    embeddings = embed_chunks(chunks, embedder)
    relevant_chunks = retrieve_relevant_chunks(query, chunks, embeddings, embedder, top_k=3)
    context = "\n".join(relevant_chunks)
    internal_prompt = f"Prompt: {query}\n\nContext:\n{context}\n\n"
    api_key_file = open(file_ollama_key)
    ollama_url = "https://ollama.com/api/generate"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key_file.read()}"}
    api_key_file.close()
    payload = {"model": ollama_cloud_model, "prompt": internal_prompt, "stream": False}
    response = requests.post(ollama_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    response_data = response.json()
    # print(response_data.get("response"))
    response.close()
    return response_data

# testing the overall system for each audio input from mp3 file

prompt_guardrail = open(file_prompt_guardrail)
prompt_guardrail_read = prompt_guardrail.read()
prompt_guardrail.close()
rag_summary1_json = None

prompt_user_sentiment = open(file_prompt_sentiment)
prompt_user_sentiment_read = prompt_user_sentiment.read()
prompt_user_sentiment.close()
rag_summary2_json = None



# check for guard rail breach
def guardrail_check(customer_query):
    global prompt_guardrail_read
    global rag_summary1_json
    try:
        rag_summary1 = rag_summarize(document_text=prompt_guardrail_read, query=customer_query)
        rag_summary1_json = json.loads(rag_summary1["response"])
        print("RAG Summary is: " + str(rag_summary1_json))
        print(rag_summary1_json["guardrail_status"])
    except Exception as e:
        print(e)
        print("RAG summary error occurred during guardrails analysis")
        return "Guardrail exception"

    if rag_summary1_json["guardrail_status"] == guardrails_breach:
        return "GUARDRAILS_BREACH"
    else:
        return "Guardrail Pass"


def sentiment_check(customer_query):
    global prompt_user_sentiment_read
    global rag_summary2_json
    # check for user query sentiment
    try:
        rag_summary = rag_summarize(document_text=prompt_user_sentiment_read, query=customer_query)
        rag_summary = rag_summary["response"]
        rag_summary = "{" + rag_summary.split("{", maxsplit=1)[1]
        last_index = rag_summary.rfind("}")
        rag_summary = rag_summary[:last_index] + "}"
        rag_summary2_json = json.loads(rag_summary)
        print("RAG Summary is: " + str(rag_summary2_json))
        print(rag_summary2_json["intent"])
    except Exception as e:
        print(e)
        print("RAG summary error occurred during sentiment analysis")
        rag_summary2_json["intent"] = "Sentiment exception"
        return "Sentiment exception"

    if rag_summary2_json["intent"] == unsupported_task_intent:
        rag_summary2_json["intent"] = "UNSUPPORTED_TASK"
        return "UNSUPPORTED_TASK"
    else:
        return "Sentiment Pass"


# parse every distorted audio -> speech to text -> check guardrail -> check sentiment -> dump in csv
idx = 0
for one_file in os.listdir(all_audio_path):
    if one_file.endswith(".mp3"):
        one_file_dst = one_file.replace(".mp3", ".wav")
        sound_mp3 = AudioSegment.from_mp3(all_audio_path + one_file)
        sound_mp3.export(all_audio_path + one_file_dst, format="wav")
        audio_stt = ""
        audio_recognizer = sr.Recognizer()
        with sr.AudioFile(all_audio_path + one_file_dst) as source:
            audio_binary = audio_recognizer.record(source)
        try:
            audio_stt = audio_recognizer.recognize_google(audio_binary)
            print("Transcribed text: " + audio_stt)
            guardrail_status = guardrail_check(audio_stt)
            sentiment_status = sentiment_check(audio_stt)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue

        # stage : IVRS action based on intent from list of supported tasks
        final_intent = rag_summary2_json["intent"]

        valid_intent = False
        match final_intent:
            case one_intent if one_intent in Check_Account_Balance:
                valid_intent = True
            case one_intent if one_intent in Review_Recent_Transactions:
                valid_intent = True
            case one_intent if one_intent in Transfer_Money:
                valid_intent = True
            case one_intent if one_intent in Pay_Bills:
                valid_intent = True
            case one_intent if one_intent in Report_Lost_or_Stolen_Card:
                valid_intent = True
            case one_intent if one_intent in Activate_New_Card:
                valid_intent = True
            case one_intent if one_intent in Request_Account_Statement:
                valid_intent = True
            case one_intent if one_intent in Check_Loan_Status:
                valid_intent = True
            case one_intent if one_intent in Stop_Cheque_Payment:
                valid_intent = True
            case one_intent if one_intent in Order_New_Cheque_Book:
                valid_intent = True
            case one_intent if one_intent in Update_Contact_Information:
                valid_intent = True
            case one_intent if one_intent in Check_Credit_Card_Limit_n_Rewards:
                valid_intent = True
            case one_intent if one_intent in Dispute_a_Transaction:
                valid_intent = True
            case one_intent if one_intent in Find_Nearest_Branch_or_ATM:
                valid_intent = True
            case one_intent if one_intent in Check_Current_Interest_Rates:
                valid_intent = True
            case one_intent if one_intent in Get_Currency_Exchange_Rates:
                valid_intent = True
            case one_intent if one_intent in Open_Fixed_or_Recurring_Deposit:
                valid_intent = True
            case one_intent if one_intent in Request_Tax_Certificates:
                valid_intent = True
            case one_intent if one_intent in Schedule_Branch_Appointment:
                valid_intent = True
            case one_intent if one_intent in Speak_to_Customer_Support_Agent:
                valid_intent = True
            # default action (wildcard)
            case _:
                valid_intent = False

        writer_csv.writerow([idx, audio_stt, guardrail_status, sentiment_status, valid_intent])
        idx+=1

my_csv.close()