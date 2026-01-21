"""Parser para transformar dados do Finpet."""

from datetime import datetime

FIELDS = {
    "id": "id_t",
    "receiptId": "receipt_id",
    "transactionNumber": "transaction_number",
    "transactionDate": "transaction_date",
    "dateReceived": "date_received",
    "dateEstimated": "date_estimated",
    "dueDate": "due_date",
    "installmentNumber": "installment_number",
    "installmentValue": "installment_value",
    "transactionValue": "transaction_value",
    "value": "value",
    "grossValue": "gross_value",
    "discountedValue": "discounted_value",
    "payedValue": "payed_value",
    "anticipateValue": "anticipate_value",
    "depositValue": "deposit_value",
    "beneficiaryValue": "beneficiary_value",
    "separatedPaymentValue": "separated_payment_value",
    "retentionValue": "retention_value",
    "fee": "fee",
    "currency": "currency",
    "status": "status",
    "product": "product",
    "processor": "processor",
    "paymentBrand": "payment_brand",
    "planType": "plan_type",
    "type": "type",
    "clientName": "client_name",
    "clientPhone": "client_phone",
    "cpf": "cpf",
    "merchant": "merchant",
    "merchantDocument": "merchant_document",
    "merchantUserEmail": "merchant_user_email",
    "userName": "user_name",
    "beneficiary": "beneficiary",
    "beneficiaryDocument": "beneficiary_document",
    "beneficiaryType": "beneficiary_type",
    "bank": "bank",
    "bankAgency": "bank_agency",
    "depositAccount": "deposit_account",
    "nsu": "nsu",
    "authorizationNumber": "authorization_number",
    "lastFourCardDigits": "last_four_card_digits",
    "urExternalReference": "ur_external_reference",
    "retentionReason": "retention_reason",
    "isBlocked": "is_blocked",
    "hasChargeback": "has_chargeback",
    "notAnticipatable": "not_anticipatable",
    "hasContractApplied": "has_contract_applied",
}

DATE_FIELDS = {"transaction_date", "date_received", "date_estimated", "due_date"}
FLOAT_FIELDS = {
    "installment_value",
    "transaction_value",
    "value",
    "gross_value",
    "discounted_value",
    "payed_value",
    "anticipate_value",
    "deposit_value",
    "beneficiary_value",
    "separated_payment_value",
    "retention_value",
    "fee",
}
BOOL_FIELDS = {
    "is_blocked",
    "has_chargeback",
    "not_anticipatable",
    "has_contract_applied",
}


def parse(raw: dict) -> dict:
    """Transforma um registro raw para o formato do PocketBase."""
    result = {}
    for src, dst in FIELDS.items():
        val = raw.get(src)
        if val is None or val == "-":
            val = None

        if dst in DATE_FIELDS and val:
            val = datetime.strptime(val, "%d/%m/%Y").isoformat()
        elif dst in FLOAT_FIELDS:
            val = float(val) if val else 0.0
        elif dst in BOOL_FIELDS:
            val = bool(val) if val else False

        result[dst] = val
    return result


def parse_all(raw_list: list) -> list:
    """Transforma uma lista de registros raw."""
    return [parse(t) for t in raw_list]
