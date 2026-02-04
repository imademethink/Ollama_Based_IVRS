# Ollama Unleashed: Ollama based Next-Gen Secure IVRS powered by Ollama, RAG, Sentiment analysis, Guardrails

# YouTube video link : https://youtu.be/NMJUvWiH8gc

<img width="1536" height="1024" alt="Thumbnail" src="https://github.com/user-attachments/assets/892fb6a6-9665-4759-96c9-de777b3556a6" />

Ollama AI model assisted mechanism suitable for IVRS (banking domain)

It uses popular AI model gpt-oss:120b-cloud (user by OpenAI)

Gemini full discussion link : https://gemini.google.com/share/9653f6bde3fa


# Features
1) Customer validation

2) Understanding Customer Intent

3) Max 3 attempt then graceful exit

4) AI Bot response based on query

5) Know Intent + Tone

6) Apply Guard Rail

7) Unsupported task handling

8) Graceful exit

# Supported tasks

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


# Supported Guardrails

1. No "Financial Advice" Constraint: Strictly prohibit the AI from providing investment recommendations, stock tips, or tax advice; force a redirect to a licensed human advisor for such queries.

2. Competitor Mention Blocking: recognizing and neutralizing queries about competitors, ensuring the system does not promote or discuss rival banks' products.

3. Sentiment-Based Escalation: Automatically transfer the call to a human agent if the customer's sentiment score drops below a specific threshold (detecting anger or distress).

4. Trusted or Allowed Topic list: Restrict the AI's knowledge base strictly to banking domain topics; reject requests to discuss politics, religion, or general trivia.

5. Confidence Thresholding: If the AI’s confidence in an answer is below a set percentage (e.g., 85%), it must fallback to a clarification question or human transfer rather than guessing.

6. Hallucination Grounding Checks: Use Retrieval-Augmented Generation (RAG) with a strict "citation" requirement; if the AI cannot find the answer in its approved document store, it must say "I don't know."

7. Toxic Language Filtering: Filter both input and output for profanity, hate speech, or abusive language, issuing a warning or terminating the call if necessary.

8. Transaction Value Limits: Hard-code maximum limits for AI-initiated transactions (e.g., transfers under $500 only); anything above requires human approval or multi-factor authentication.

9. Regulatory Disclaimers: Mandate that the system self-identifies as an artificial intelligence at the start of the interaction and whenever asked, complying with transparency laws.

10. Emergency & Crisis Protocol: If keywords related to self-harm, physical threats, or extreme distress are detected, immediately route to a specialized human team or provide emergency contact numbers.

11. Bias Mitigation Filters: specific checks to ensure responses regarding loans or credit do not vary based on inferred demographics (race, gender, accent) of the caller.

12. Rate Limiting & Anti-Spam: Limit the number of queries or transactions a single caller can perform in a short window to prevent Denial of Service (DoS) or brute-force attacks.

13. Output Conciseness Enforcer: Limit the length of AI responses to prevent rambling; force answers to be brief (e.g., under 30 words) to suit the auditory nature of IVR.

14. Sensitive Action Confirmation: Require an explicit "Yes/No" verbal confirmation from the user before executing any state-changing action (e.g., "Are you sure you want to block this card?").

15. Audit Trail Immutability: rigorous logging of every AI decision and user input in a "Write Once, Read Many" (WORM) format for compliance auditing and forensic analysis.



# Steps
As explained in above YouTube video, install Ollama (Windows/ Linux), get the API key

Store the key in ollama_api_key_file.txt

Download cloud AI model using : ollama run gpt-oss:120b-cloud

git clone https://github.com/imademethink/Ollama_Based_IVRS.git

cd Ollama_Based_IVRS-main

pip install -r requirements.txt

python ivrs1_dev.py

python ivrs2_qa.py

# Note : Strictly use Python 3.11 version 


