import asyncio
import json
import signal
import ssl
import hashlib
import random
import ast
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple, TypedDict

import certifi
import requests
import websockets
from print_color import print

# ========================== #
# Fill in your details here  #
# ========================== #
USERNAME = ""
PASSWORD = ""
# ========================== #
# Fill in your details here  #
# ========================== #

currenciesDict = {
    "USDUSD": 1.000000000,
    "EURUSD": 1.080000000,
    "JPYUSD": 0.006700000,
    "GBPUSD": 1.270000000,
    "AUDUSD": 0.660000000,
    "CADUSD": 0.740000000,
    "CHFUSD": 1.100000000,
    "CNYUSD": 0.140000000,
    "SEKUSD": 0.093000000,
    "NZDUSD": 0.610000000,
    "MXNUSD": 0.058000000,
    "SGDUSD": 0.740000000,
    "HKDUSD": 0.130000000,
    "NOKSGD": 0.124324324,
    "NOKSEK": 0.989247312,
    "KRWAUD": 0.001136364,
    "KRWCAD": 0.001013514,
    "TRYCNY": 0.221428571,
    "INRCNY": 0.085714286,
    "INRKRW": 16.000000000,
    "BRLKRW": 253.333333333,
    "BRLMXN": 3.275862069,
    "ZARHKD": 0.407692308,
    "RUBMXN": 0.189655172,
    "DKKBRL": 0.736842105,
    "DKKCAD": 0.189189189,
    "PLNINR": 20.833333333,
    "PLNHKD": 1.923076923,
    "THBKRW": 36.000000000,
    "THBPLN": 0.108000000,
    "IDRZAR": 0.001169811,
    "IDRCAD": 0.000083784,
    "HUFTRY": 0.090322581,
    "HUFSEK": 0.030107527,
    "CZKMXN": 0.741379310,
    "CZKINR": 3.583333333,
    "ILSSGD": 0.364864865,
    "CLPMXN": 0.018965517,
    "CLPINR": 0.091666667,
    "PHPKRW": 24.000000000,
    "PHPCZK": 0.418604651,
    "AEDCHF": 0.245454545,
    "AEDINR": 22.500000000,
    "COPRUB": 0.023636364,
    "SARZAR": 5.094339623,
    "SARCAD": 0.364864865,
    "MYRINR": 17.500000000,
    "MYRRUB": 19.090909091,
    "RONPLN": 0.880000000,
    "RONHUF": 78.571428571,
    "PENRON": 1.227272727,
    "PENTHB": 10.000000000,
    "ARSEUR": 0.001111111,
    "EGPPEN": 0.077777778,
    "NGNCAD": 0.000905405,
    "BDTCZK": 0.211627907,
    "BDTMYR": 0.043333333,
    "VNDTHB": 0.001444444,
    "USDEUR": 0.925925926,
    "USDJPY": 149.253731343,
    "USDGBP": 0.787401575,
    "USDAUD": 1.515151515,
    "USDCAD": 1.351351351,
    "USDCHF": 0.909090909,
    "USDCNY": 7.142857143,
    "USDSEK": 10.752688172,
    "USDNZD": 1.639344262,
    "USDMXN": 17.241379310,
    "USDSGD": 1.351351351,
    "USDHKD": 7.692307692,
    "SGDNOK": 8.043478261,
    "SEKNOK": 1.010869565,
    "AUDKRW": 880.000000000,
    "CADKRW": 986.666666667,
    "CNYTRY": 4.516129032,
    "CNYINR": 11.666666667,
    "KRWINR": 0.062500000,
    "KRWBRL": 0.003947368,
    "MXNBRL": 0.305263158,
    "HKDZAR": 2.452830189,
    "MXNRUB": 5.272727273,
    "BRLDKK": 1.357142857,
    "CADDKK": 5.285714286,
    "INRPLN": 0.048000000,
    "HKDPLN": 0.520000000,
    "KRWTHB": 0.027777778,
    "PLNTHB": 9.259259259,
    "ZARIDR": 854.838709677,
    "CADIDR": 11935.483870968,
    "TRYHUF": 11.071428571,
    "SEKHUF": 33.214285714,
    "MXNCZK": 1.348837209,
    "INRCZK": 0.279069767,
    "SGDILS": 2.740740741,
    "MXNCLP": 52.727272727,
    "INRCLP": 10.909090909,
    "KRWPHP": 0.041666667,
    "CZKPHP": 2.388888889,
    "CHFAED": 4.074074074,
    "INRAED": 0.044444444,
    "RUBCOP": 42.307692308,
    "ZARSAR": 0.196296296,
    "CADSAR": 2.740740741,
    "INRMYR": 0.057142857,
    "RUBMYR": 0.052380952,
    "PLNRON": 1.136363636,
    "HUFRON": 0.012727273,
    "RONPEN": 0.814814815,
    "THBPEN": 0.100000000,
    "EURARS": 900.000000000,
    "PENEGP": 12.857142857,
    "CADNGN": 1104.477611940,
    "CZKBDT": 4.725274725,
    "MYRBDT": 23.076923077,
    "THBVND": 692.307692308,
}

def perform_conversion(sourceCurrency: str, targetCurrency: str):
    key = sourceCurrency + targetCurrency
    if key in currenciesDict:
        return currenciesDict[key]
    else:
        return None

@dataclass(frozen=True)
class TransactionLimit:
    amount: float
    currency: str

@dataclass(frozen=True)
class CardDetails:
    cardId: str
    accountId: str
    issuedLocation: str
    number: str
    expiryMonth: int
    expiryYear: int
    cvv: int
    checksum: str
    transactionLimit: TransactionLimit
    dynamicRules: list

@dataclass(frozen=True)
class Transaction:
    id: str
    transactionId: str
    transactionCurrency: str
    transactionAmount: float
    merchant: str
    cardDetails: CardDetails

class ApprovalDecision(TypedDict):
    id: str
    approval: bool

# Global history for repeat (safe) transactions (Check 4)
safe_history = set()

# South American country codes
countries = ["AR", "BO", "BR", "CL", "CO", "EC", "GY", "PY", "PE", "SR", "UY", "VE"]

# Enterprise bins (first six digits)
enterprise_bins = [402633, 552187, 370002, 601105, 455938, 520091, 340788, 644003]

def log(transaction: Transaction):
    with open("transaction.log", "a") as fio:
        fio.write(str(transaction) + "\n")

def parse_merchant(name: str):
    # Merchant encoding:
    # First 3 digits: length of non-junk characters that follow
    # Next 4: merchant category code (MCC)
    # Next variable: merchant name (until the last 2 characters)
    # Last 2: country code
    Length = int(name[0:3])
    final = 3 + Length
    non_junk = name[:final]
    mcc = non_junk[3:3+4]
    merchant_name = non_junk[7:final-2]
    country = non_junk[final-2:final]
    # Debug print; remove if not needed.
    print(f"Parsed merchant -> MCC: {mcc}, Name: {merchant_name}, Country: {country}")
    return [mcc, merchant_name, country]

def is_legacy_card(card: CardDetails) -> bool:
    now = datetime.now()
    try:
        expiry_date = datetime(card.expiryYear, card.expiryMonth, 1)
    except Exception as e:
        return False
    # If the card expires between now and 12 months from now (inclusive)
    if now <= expiry_date <= now + timedelta(days=365):
        return True
    return False

def is_checksum_valid(card: CardDetails) -> bool:
    # The checksum is computed by concatenating card number, expiry month (2 digits),
    # last two digits of expiry year, and cvv, then hashing using SHA-256.
    expiryMonth = f"{card.expiryMonth:02d}"
    expiryYear = str(card.expiryYear)[-2:]
    prehash = f"{card.number}{expiryMonth}{expiryYear}{card.cvv}"
    computed = hashlib.sha256(prehash.encode('utf-8')).hexdigest()
    return computed == card.checksum

def has_increasing_subsequence(number: str, subseq_len: int = 7) -> bool:
    # Check for a strictly increasing subsequence (not necessarily contiguous)
    digits = [int(d) for d in number if d.isdigit()]
    n = len(digits)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if digits[j] < digits[i]:
                dp[i] = max(dp[i], dp[j] + 1)
                if dp[i] >= subseq_len:
                    return True
    return False

def evaluate_dynamic_rule(rule: str, transaction: Transaction) -> bool:
    # Expected rule format:
    # "propertyName [NOT] operator value"
    tokens = rule.split()
    negate = False
    if len(tokens) < 3:
        return False  # Malformed rule
    if tokens[1] == "NOT":
        property_name = tokens[0]
        operator = tokens[2]
        value_token = " ".join(tokens[3:])
        negate = True
    else:
        property_name = tokens[0]
        operator = tokens[1]
        value_token = " ".join(tokens[2:])

    # Parse value (if operator is IN, expect a list)
    try:
        if operator == "IN":
            value = ast.literal_eval(value_token)
        else:
            try:
                value = float(value_token)
            except ValueError:
                value = value_token
    except Exception as e:
        value = value_token

    # Retrieve the actual value from transaction or its cardDetails.
    actual = None
    if hasattr(transaction, property_name):
        actual = getattr(transaction, property_name)
    elif hasattr(transaction.cardDetails, property_name):
        actual = getattr(transaction.cardDetails, property_name)
    else:
        # Property not found; rule fails.
        return False

    # Apply the operator.
    try:
        if operator == "=":
            result = (actual == value)
        elif operator == "<":
            result = (float(actual) < float(value))
        elif operator == ">":
            result = (float(actual) > float(value))
        elif operator == "IN":
            result = (actual in value)
        else:
            result = False
    except Exception as e:
        result = False

    return not result if negate else result

def should_process(transaction: Transaction) -> bool:
    log(transaction)
    print("_________________________")
    print(transaction)

    card_account = (transaction.cardDetails.cardId, transaction.cardDetails.accountId)
    # Check 4: Repeat Customer Transactions
    if card_account in safe_history:
        print("Repeat customer found; automatically safe.")
        return True

    # Check 1: Merchant Validity
    merchant = parse_merchant(transaction.merchant)
    mcc_str, merchant_name, merchant_country = merchant

    # Rule 4: Merchant name does not contain letter 'E' (case-insensitive)
    if "E" not in merchant_name.upper():
        print("Merchant name does not contain 'E'; safe.")
        safe_history.add(card_account)
        return True

    # Rule 1: Merchant country in South America
    if merchant_country in countries:
        print("Merchant is in South America; safe.")
        safe_history.add(card_account)
        return True

    # Rule 3: Merchant Category Code indicating an airline (3000 <= MCC <= 3308)
    try:
        mcc = int(mcc_str)
        if 3000 <= mcc <= 3308:
            print("Merchant MCC indicates an airline; safe.")
            safe_history.add(card_account)
            return True
    except Exception:
        pass

    # Rule 2: Card issued location matches merchant country
    if transaction.cardDetails.issuedLocation == merchant_country:
        print("Card issued location matches merchant country; safe.")
        safe_history.add(card_account)
        return True

    # Check 2: Card Validity

    # Rule 1: Card BIN is from an Enterprise customer
    try:
        if int(transaction.cardDetails.number[:6]) in enterprise_bins:
            print("Card BIN is Enterprise; safe.")
            safe_history.add(card_account)
            return True
    except Exception:
        pass

    # Rule 2: Legacy card (expires within next 12 months)
    if is_legacy_card(transaction.cardDetails):
        print("Card is a legacy card; safe.")
        safe_history.add(card_account)
        return True

    # Rule 3: Valid checksum
    if is_checksum_valid(transaction.cardDetails):
        print("Card checksum is valid; safe.")
        safe_history.add(card_account)
        return True

    # Rule 4: PAN contains a strictly increasing subsequence of length >= 7
    if has_increasing_subsequence(transaction.cardDetails.number):
        print("Card number has an increasing subsequence; safe.")
        safe_history.add(card_account)
        return True

    # Check 3: Transaction Limit
    if transaction.transactionCurrency == "USD":
        amount_usd = transaction.transactionAmount
    else:
        rate = perform_conversion(transaction.transactionCurrency, "USD")
        if rate is not None:
            amount_usd = transaction.transactionAmount * rate
        else:
            amount_usd = transaction.transactionAmount  # Fallback
    if amount_usd < transaction.cardDetails.transactionLimit.amount:
        print("Transaction amount is below the limit; safe.")
        safe_history.add(card_account)
        return True

    # Check 5: Dynamic Rules
    dynamic_rules = transaction.cardDetails.dynamicRules
    if dynamic_rules:
        all_pass = True
        for rule in dynamic_rules:
            if not evaluate_dynamic_rule(rule, transaction):
                print(f"Dynamic rule failed: {rule}")
                all_pass = False
                break
        if all_pass:
            print("All dynamic rules passed; safe.")
            safe_history.add(card_account)
            return True
    else:
        # No dynamic rules implies they all pass.
        print("No dynamic rules present; considered safe.")
        safe_history.add(card_account)
        return True

    # If none of the checks pass, then the transaction is not safe.
    print("Transaction did not pass any safety check; not safe.")
    return False

def parse_transaction(message: str) -> Transaction | None:
    if message.startswith('{"id"'):
        try:
            transaction_data = json.loads(message)
            card_details_data = transaction_data.pop("cardDetails", {})
            transaction_limit_data = card_details_data.pop("transactionLimit", {})
            transaction_limit = TransactionLimit(**transaction_limit_data)
            dynamic_rules = card_details_data.pop("dynamicRules", [])
            card_details = CardDetails(
                **card_details_data, transactionLimit=transaction_limit, dynamicRules=dynamic_rules
            )
            transaction = Transaction(**transaction_data, cardDetails=card_details)
            return transaction
        except json.JSONDecodeError:
            print("Failed to decode JSON message:", message, color="magenta")
            return None
        except KeyError as e:
            print(f"Missing key in transaction data: {e}", color="magenta")
            return None
    else:
        print("Non-transaction message received:", message, color="yellow")
        return None

def handle_transaction(transaction: Transaction) -> ApprovalDecision:
    decision: ApprovalDecision = {
        "id": transaction.id,
        "approval": should_process(transaction),
    }
    return decision

APP_URL = "https://awx-detective-7bytp.ondigitalocean.app/api/v1/login"
WEBSOCKET_URL = "wss://awx-detective-7bytp.ondigitalocean.app/api/v1/transaction_feed"

async def listen_to_transactions(ssl_context: ssl.SSLContext, jwt: str) -> None:
    headers = {"Authorization": f"Bearer {jwt}"}
    async with websockets.connect(
        WEBSOCKET_URL, additional_headers=headers, ssl=ssl_context
    ) as websocket:
        try:
            async for message in websocket:
                transaction = parse_transaction(message)  # type: ignore
                if transaction:
                    decision = handle_transaction(transaction)
                    await websocket.send(json.dumps(decision))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e.code}", color="magenta")
        except Exception as e:
            print(f"Error: {e}", color="magenta")

def setup_and_auth() -> Tuple[ssl.SSLContext, str]:
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    payload = json.dumps({"username": USERNAME, "password": PASSWORD})
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", APP_URL, headers=headers, data=payload)
    try:
        data = json.loads(response.text)
    except Exception as e:
        raise ValueError("Incorrect Username Or Password!", e)
    jwt = data.get("token")
    return ssl_context, jwt

async def shutdown(loop) -> None:
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def main() -> None:
    loop = asyncio.new_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))
    try:
        ssl_context, jwt = setup_and_auth()
        loop.run_until_complete(listen_to_transactions(ssl_context, jwt))
    except asyncio.exceptions.CancelledError:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main()
