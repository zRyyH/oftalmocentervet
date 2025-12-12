"""Parser de transações Finpet."""

from datetime import datetime
from typing import Any


def parse_date(value: Any) -> str | None:
    if not value or value == "-":
        return None
    return datetime.strptime(value, "%d/%m/%Y").isoformat()


def parse_float(value: Any) -> float:
    if value is None or value == "-":
        return 0.0
    return float(value)


def parse_str(value: Any) -> str | None:
    if value is None or value == "-":
        return None
    return str(value)


def parse_bool(value: Any) -> bool:
    if value is None:
        return False
    return bool(value)


def parse_transaction(raw: dict) -> dict:
    return {
        "id_t": parse_str(raw.get("id")),
        "receipt_id": parse_str(raw.get("receiptId")),
        "transaction_number": parse_str(raw.get("transactionNumber")),
        "transaction_date": parse_date(raw.get("transactionDate")),
        "date_received": parse_date(raw.get("dateReceived")),
        "date_estimated": parse_date(raw.get("dateEstimated")),
        "due_date": parse_date(raw.get("dueDate")),
        "installment_number": parse_str(raw.get("installmentNumber")),
        "installment_value": parse_float(raw.get("installmentValue")),
        "transaction_value": parse_float(raw.get("transactionValue")),
        "value": parse_float(raw.get("value")),
        "gross_value": parse_float(raw.get("grossValue")),
        "discounted_value": parse_float(raw.get("discountedValue")),
        "payed_value": parse_float(raw.get("payedValue")),
        "anticipate_value": parse_float(raw.get("anticipateValue")),
        "deposit_value": parse_float(raw.get("depositValue")),
        "beneficiary_value": parse_float(raw.get("beneficiaryValue")),
        "separated_payment_value": parse_float(raw.get("separatedPaymentValue")),
        "retention_value": parse_float(raw.get("retentionValue")),
        "fee": parse_float(raw.get("fee")),
        "currency": parse_str(raw.get("currency")),
        "status": parse_str(raw.get("status")),
        "product": parse_str(raw.get("product")),
        "processor": parse_str(raw.get("processor")),
        "payment_brand": parse_str(raw.get("paymentBrand")),
        "plan_type": parse_str(raw.get("planType")),
        "type": parse_str(raw.get("type")),
        "client_name": parse_str(raw.get("clientName")),
        "client_phone": parse_str(raw.get("clientPhone")),
        "cpf": parse_str(raw.get("cpf")),
        "merchant": parse_str(raw.get("merchant")),
        "merchant_document": parse_str(raw.get("merchantDocument")),
        "merchant_user_email": parse_str(raw.get("merchantUserEmail")),
        "user_name": parse_str(raw.get("userName")),
        "beneficiary": parse_str(raw.get("beneficiary")),
        "beneficiary_document": parse_str(raw.get("beneficiaryDocument")),
        "beneficiary_type": parse_str(raw.get("beneficiaryType")),
        "bank": parse_str(raw.get("bank")),
        "bank_agency": parse_str(raw.get("bankAgency")),
        "deposit_account": parse_str(raw.get("depositAccount")),
        "nsu": parse_str(raw.get("nsu")),
        "authorization_number": parse_str(raw.get("authorizationNumber")),
        "last_four_card_digits": parse_str(raw.get("lastFourCardDigits")),
        "ur_external_reference": parse_str(raw.get("urExternalReference")),
        "retention_reason": parse_str(raw.get("retentionReason")),
        "is_blocked": parse_bool(raw.get("isBlocked")),
        "has_chargeback": parse_bool(raw.get("hasChargeback")),
        "not_anticipatable": parse_bool(raw.get("notAnticipatable")),
        "has_contract_applied": parse_bool(raw.get("hasContractApplied")),
    }


def parse_transactions(raw_list: list[dict]) -> list[dict]:
    return [parse_transaction(t) for t in raw_list]
