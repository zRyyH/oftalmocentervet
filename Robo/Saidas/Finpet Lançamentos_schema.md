# JSON Schema: `Finpet Lançamentos.json`

## Resumo

- **Tipo raiz:** `array`
- **Total de registros:** 371
- **Campos únicos:** 105

## Estrutura

```
item: object
  comparacoes: object
    auth: object
      auths_encontrados: array
        auths_encontrados[*]: string <numeric_string>
      finpet: string <numeric_string>
      match: boolean
      release: null|string <numeric_string>
    cliente: object
      finpet: array
        finpet[*]: string <numeric_string>
      match: boolean
      release: string
    data: object
      finpet_estimated: string <datetime_iso>
      match: boolean
      release: null|string <datetime_iso>
    parcela: object
      finpet: string
      match: boolean
      release: null|string
    tipo: object
      finpet: string
      match: boolean
      release: null|string
    valor: object
      exact_value: boolean
      finpet: integer|number
      match: boolean
      release: integer|null|number
  finpet: object
    anticipate_value: integer
    authorization_number: string <numeric_string>
    bank: string
    bank_agency: string <numeric_string>
    beneficiary: string
    beneficiary_document: string <phone>
    beneficiary_type: string
    beneficiary_value: integer|number
    client_name: string
    client_phone: string
    collection_id: string
    collection_name: string
    cpf: string <phone>
    created: string <datetime_iso>
    currency: string
    date_estimated: string <datetime_iso>
    date_received: string <datetime_iso>
    deposit_account: string
    deposit_value: integer|number
    discounted_value: integer|number
    due_date: string <datetime_iso>
    expand: object
    fee: number
    gross_value: integer|number
    has_chargeback: boolean
    has_contract_applied: boolean
    id: string
    id_t: string
    installment_number: string
    installment_value: integer|number
    is_blocked: boolean
    last_four_card_digits: string <numeric_string>
    merchant: string
    merchant_document: string <phone>
    merchant_user_email: string <email>
    not_anticipatable: boolean
    nsu: string <numeric_string>
    payed_value: integer|number
    payment_brand: string
    plan_type: string
    processor: string
    product: string
    receipt_id: string
    retention_reason: string
    retention_value: integer|number
    separated_payment_value: integer|number
    status: string
    transaction_date: string <datetime_iso>
    transaction_number: string <numeric_string>
    transaction_value: integer|number
    type: string
    updated: string <datetime_iso>
    ur_external_reference: string
    user_name: string
    value: integer|number
  release: null|object
    collection_id: string
    collection_name: string
    created: string <datetime_iso>
    data: string <datetime_iso>
    descricao: string
    expand: object
    forma_pagamento: string
    fornecedor: string
    id: string
    id_r: string <numeric_string>
    origem: string
    parcela: string
    status: string
    tipo: string
    updated: string <datetime_iso>
    valor: integer|number
    vencimento: string <datetime_iso>
  score: integer
```

## Campos

### `item`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.auth`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.auth.auths_encontrados`

- **Tipo:** array
- **Ocorrências:** 358
- **Tamanho:** 0 - 3 items

### `item.comparacoes.auth.auths_encontrados[]`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 503
- **Comprimento:** 6 - 6 chars
- **Exemplos:** `SUZANA`, `382852`, `540963`

### `item.comparacoes.auth.finpet`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 6 - 6 chars
- **Exemplos:** `130261`, `382852`, `540963`

### `item.comparacoes.auth.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `False`, `True`

### `item.comparacoes.auth.release`

- **Tipo:** null, string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Nulos:** 44
- **Comprimento:** 6 - 6 chars
- **Exemplos:** `382852`, `540963`, `130261`

### `item.comparacoes.cliente`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.cliente.finpet`

- **Tipo:** array
- **Ocorrências:** 371
- **Tamanho:** 0 - 2 items

### `item.comparacoes.cliente.finpet[]`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 374
- **Comprimento:** 4 - 5 chars
- **Exemplos:** `8454`, `12642`, `12628`

### `item.comparacoes.cliente.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `True`, `False`

### `item.comparacoes.cliente.release`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 0 - 98 chars
- **Exemplos:** `Baixa parcial venda 8454 - Suzana - Caixa 772 0002585141`, `Baixa venda 12642 - Cláudia - Caixa 1163 382852`, `Baixa venda 12628 - MARIA - Caixa 1163 540963`

### `item.comparacoes.data`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.data.finpet_estimated`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2025-11-24 00:00:00.000Z`, `2025-11-25 00:00:00.000Z`, `2025-11-26 00:00:00.000Z`

### `item.comparacoes.data.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `False`, `True`

### `item.comparacoes.data.release`

- **Tipo:** null, string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Nulos:** 13
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2026-01-01 00:00:00.000Z`, `2025-12-24 00:00:00.000Z`, `2025-11-24 00:00:00.000Z`

### `item.comparacoes.parcela`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.parcela.finpet`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 3 - 5 chars
- **Exemplos:** `9/10`, `1/6`, `1/2`

### `item.comparacoes.parcela.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `True`, `False`

### `item.comparacoes.parcela.release`

- **Tipo:** null, string
- **Ocorrências:** 371
- **Nulos:** 13
- **Comprimento:** 3 - 5 chars
- **Exemplos:** `9/10`, `1/6`, `1/2`

### `item.comparacoes.tipo`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.tipo.finpet`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 8 - 8 chars
- **Exemplos:** `MERCHANT`, `SUPPLIER`

### `item.comparacoes.tipo.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `True`, `False`

### `item.comparacoes.tipo.release`

- **Tipo:** null, string
- **Ocorrências:** 371
- **Nulos:** 13
- **Comprimento:** 7 - 7 chars
- **Exemplos:** `receita`, `despesa`

### `item.comparacoes.valor`

- **Tipo:** object
- **Ocorrências:** 371

### `item.comparacoes.valor.exact_value`

- **Tipo:** boolean
- **Ocorrências:** 358
- **Exemplos:** `True`, `False`

### `item.comparacoes.valor.finpet`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.55`

### `item.comparacoes.valor.match`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `True`, `False`

### `item.comparacoes.valor.release`

- **Tipo:** integer, null, number
- **Ocorrências:** 371
- **Nulos:** 13
- **Range:** -1200 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.54`

### `item.finpet`

- **Tipo:** object
- **Ocorrências:** 371

### `item.finpet.anticipate_value`

- **Tipo:** integer
- **Ocorrências:** 371
- **Range:** 0 → 0
- **Exemplos:** `0`

### `item.finpet.authorization_number`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 6 - 6 chars
- **Exemplos:** `130261`, `382852`, `540963`

### `item.finpet.bank`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 4 - 32 chars
- **Exemplos:** `Banco Cooperativo do Brasil S.A.`, `Banco do Brasil`, `C6 Bank`

### `item.finpet.bank_agency`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 4 - 6 chars
- **Exemplos:** `3214`, `0269-0`, `0001`

### `item.finpet.beneficiary`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 15 - 52 chars
- **Exemplos:** `Oftalmologia Veterinaria Mamede E Tasso LTDA FINPET`, `Ivan Ricardo Martinez Padua`, `Gabrielle Bianca Armellino`

### `item.finpet.beneficiary_document`

- **Tipo:** string
- **Formato:** phone
- **Ocorrências:** 371
- **Comprimento:** 11 - 14 chars
- **Exemplos:** `14371342000122`, `23325617816`, `45855504883`

### `item.finpet.beneficiary_type`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 21 - 21 chars
- **Exemplos:** `PAYMENT_TYPE_MERCHANT`, `PAYMENT_TYPE_SUPPLIER`

### `item.finpet.beneficiary_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `0`, `364.55`, `810.1`

### `item.finpet.client_name`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 2 - 20 chars
- **Exemplos:** `VENDAS 8454`, `VENDA 12642`, `VENDA 12628`

### `item.finpet.client_phone`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 0 - 15 chars
- **Exemplos:** ``, `(16) 99639-3533`

### `item.finpet.collection_id`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 16 - 16 chars
- **Exemplos:** `a7b3c9d2e5f8g1h4`

### `item.finpet.collection_name`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 6 - 6 chars
- **Exemplos:** `finpet`

### `item.finpet.cpf`

- **Tipo:** string
- **Formato:** phone
- **Ocorrências:** 371
- **Comprimento:** 0 - 11 chars
- **Exemplos:** ``, `94663980830`

### `item.finpet.created`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 19 - 19 chars
- **Exemplos:** `2026-01-21 12:42:11`

### `item.finpet.currency`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 3 - 3 chars
- **Exemplos:** `BRL`

### `item.finpet.date_estimated`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2025-11-24 00:00:00.000Z`, `2025-11-25 00:00:00.000Z`, `2025-11-26 00:00:00.000Z`

### `item.finpet.date_received`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 0 - 24 chars
- **Exemplos:** `2025-11-24 00:00:00.000Z`, `2025-11-25 00:00:00.000Z`, `2025-11-23 00:00:00.000Z`

### `item.finpet.deposit_account`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 7 - 10 chars
- **Exemplos:** `53790-0`, `33868-0`, `31921820-1`

### `item.finpet.deposit_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `0`, `364.55`, `810.1`

### `item.finpet.discounted_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 177.61
- **Exemplos:** `29.11`, `23.23`, `10.45`

### `item.finpet.due_date`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2025-11-24 00:00:00.000Z`, `2025-11-25 00:00:00.000Z`, `2025-11-26 00:00:00.000Z`

### `item.finpet.expand`

- **Tipo:** object
- **Ocorrências:** 371

### `item.finpet.fee`

- **Tipo:** number
- **Ocorrências:** 371
- **Range:** 1.1 → 3.49
- **Exemplos:** `3.49`, `2.79`, `2.3`

### `item.finpet.gross_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 2.17 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.55`

### `item.finpet.has_chargeback`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `False`

### `item.finpet.has_contract_applied`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `False`

### `item.finpet.id`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 16 - 16 chars
- **Exemplos:** `sr0xgynn3kzz52xw`, `shb6rmcd96nwyur5`, `p87omo9tbgdnnqo2`

### `item.finpet.id_t`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 12 - 12 chars
- **Exemplos:** `MjEyMzY0OTQy`, `MjQyMDkwNzYz`, `MjQyMDk0OTAz`

### `item.finpet.installment_number`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 3 - 5 chars
- **Exemplos:** `9/10`, `1/6`, `1/2`

### `item.finpet.installment_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 40 → 1890
- **Exemplos:** `834`, `833.33`, `375`

### `item.finpet.is_blocked`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `False`

### `item.finpet.last_four_card_digits`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 4 - 4 chars
- **Exemplos:** `5141`, `0433`, `8123`

### `item.finpet.merchant`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 51 - 51 chars
- **Exemplos:** `Oftalmologia Veterinaria Mamede E Tasso LTDA FINPET`

### `item.finpet.merchant_document`

- **Tipo:** string
- **Formato:** phone
- **Ocorrências:** 371
- **Comprimento:** 14 - 14 chars
- **Exemplos:** `14371342000122`

### `item.finpet.merchant_user_email`

- **Tipo:** string
- **Formato:** email
- **Ocorrências:** 371
- **Comprimento:** 22 - 22 chars
- **Exemplos:** `fabriciovm@hotmail.com`

### `item.finpet.not_anticipatable`

- **Tipo:** boolean
- **Ocorrências:** 371
- **Exemplos:** `True`

### `item.finpet.nsu`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 6 - 12 chars
- **Exemplos:** `000258`, `000201000150`, `000201000151`

### `item.finpet.payed_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `0`, `364.55`, `810.1`

### `item.finpet.payment_brand`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 3 - 18 chars
- **Exemplos:** `MasterCard`, `Visa`, `American Express`

### `item.finpet.plan_type`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 23 - 23 chars
- **Exemplos:** `FULL_STANDARD_PLAN_TYPE`

### `item.finpet.processor`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 10 - 10 chars
- **Exemplos:** `PagService`

### `item.finpet.product`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 3 - 6 chars
- **Exemplos:** `POS`, `INVITE`

### `item.finpet.receipt_id`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 12 - 12 chars
- **Exemplos:** `MjEyMzY0OTQy`, `MjQyMDkwNzYz`, `MjQyMDk0OTAz`

### `item.finpet.retention_reason`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 0 - 27 chars
- **Exemplos:** ``, `Retenção sobre Split Finpet`

### `item.finpet.retention_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 168.89
- **Exemplos:** `0`, `40.92`, `43.97`

### `item.finpet.separated_payment_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.55`

### `item.finpet.status`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 4 - 17 chars
- **Exemplos:** `PAID`, `SCHEDULED_PAYMENT`, `UNPAID`

### `item.finpet.transaction_date`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2025-02-25 00:00:00.000Z`, `2025-10-23 00:00:00.000Z`, `2025-10-24 00:00:00.000Z`

### `item.finpet.transaction_number`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 371
- **Comprimento:** 19 - 19 chars
- **Exemplos:** `5112505325022551721`, `5693208825102351721`, `5693285125102351721`

### `item.finpet.transaction_value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 40 → 8340
- **Exemplos:** `8340`, `5000`, `750`

### `item.finpet.type`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 8 - 8 chars
- **Exemplos:** `MERCHANT`, `SUPPLIER`

### `item.finpet.updated`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 371
- **Comprimento:** 19 - 19 chars
- **Exemplos:** `2026-01-21 12:42:11`

### `item.finpet.ur_external_reference`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 36 - 42 chars
- **Exemplos:** `14371342000122_20251124_MCC_14371342000122`, `23325617816_20251124_MCC_23325617816`, `14371342000122_20251125_VCC_14371342000122`

### `item.finpet.user_name`

- **Tipo:** string
- **Ocorrências:** 371
- **Comprimento:** 23 - 23 chars
- **Exemplos:** `Fabricio Villela Mamede`

### `item.finpet.value`

- **Tipo:** integer, number
- **Ocorrências:** 371
- **Range:** 0 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.55`

### `item.release`

- **Tipo:** null, object
- **Ocorrências:** 371
- **Nulos:** 13

### `item.release.collection_id`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 13 - 13 chars
- **Exemplos:** `pbc_953728200`

### `item.release.collection_name`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 8 - 8 chars
- **Exemplos:** `releases`

### `item.release.created`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 358
- **Comprimento:** 19 - 19 chars
- **Exemplos:** `2026-01-21 12:42:31`, `2026-01-21 12:42:32`

### `item.release.data`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 358
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2026-01-01 00:00:00.000Z`, `2025-12-24 00:00:00.000Z`, `2025-11-24 00:00:00.000Z`

### `item.release.descricao`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 37 - 98 chars
- **Exemplos:** `Baixa parcial venda 8454 - Suzana - Caixa 772 0002585141`, `Baixa venda 12642 - Cláudia - Caixa 1163 382852`, `Baixa venda 12628 - MARIA - Caixa 1163 540963`

### `item.release.expand`

- **Tipo:** object
- **Ocorrências:** 358

### `item.release.forma_pagamento`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 0 - 3 chars
- **Exemplos:** `CRE`, ``, `DEB`

### `item.release.fornecedor`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 7 - 32 chars
- **Exemplos:** `Finpet Master Card Crédito`, `Ivan Ricardo Martinez Padua`, `Finpet Visa Crédito`

### `item.release.id`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 15 - 15 chars
- **Exemplos:** `7zr89cqs5e1ajk6`, `zillyngmbhy8aec`, `25orei6eyhafj69`

### `item.release.id_r`

- **Tipo:** string
- **Formato:** numeric_string
- **Ocorrências:** 358
- **Comprimento:** 9 - 9 chars
- **Exemplos:** `330775253`, `402637937`, `402638781`

### `item.release.origem`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 0 - 3 chars
- **Exemplos:** `VEN`, ``

### `item.release.parcela`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 0 - 8 chars
- **Exemplos:** `9 de 10`, `1 de 6`, `1 de 2`

### `item.release.status`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 1 - 1 chars
- **Exemplos:** `P`, `A`, `N`

### `item.release.tipo`

- **Tipo:** string
- **Ocorrências:** 358
- **Comprimento:** 7 - 7 chars
- **Exemplos:** `receita`, `despesa`

### `item.release.updated`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 358
- **Comprimento:** 19 - 19 chars
- **Exemplos:** `2026-01-21 12:42:31`, `2026-01-21 12:42:32`

### `item.release.valor`

- **Tipo:** integer, number
- **Ocorrências:** 358
- **Range:** -1200 → 1846.53
- **Exemplos:** `804.89`, `810.1`, `364.54`

### `item.release.vencimento`

- **Tipo:** string
- **Formato:** datetime_iso
- **Ocorrências:** 358
- **Comprimento:** 24 - 24 chars
- **Exemplos:** `2026-01-01 00:00:00.000Z`, `2025-12-24 00:00:00.000Z`, `2025-11-24 00:00:00.000Z`

### `item.score`

- **Tipo:** integer
- **Ocorrências:** 371
- **Range:** 0 → 5
- **Exemplos:** `3`, `4`, `5`

## Análise de Obrigatoriedade

**Obrigatórios:** `item`, `item.comparacoes`, `item.comparacoes.auth`, `item.comparacoes.auth.finpet`, `item.comparacoes.auth.match`, `item.comparacoes.auth.release`, `item.comparacoes.cliente`, `item.comparacoes.cliente.finpet`, `item.comparacoes.cliente.match`, `item.comparacoes.cliente.release`, `item.comparacoes.data`, `item.comparacoes.data.finpet_estimated`, `item.comparacoes.data.match`, `item.comparacoes.data.release`, `item.comparacoes.parcela`, `item.comparacoes.parcela.finpet`, `item.comparacoes.parcela.match`, `item.comparacoes.parcela.release`, `item.comparacoes.tipo`, `item.comparacoes.tipo.finpet`, `item.comparacoes.tipo.match`, `item.comparacoes.tipo.release`, `item.comparacoes.valor`, `item.comparacoes.valor.finpet`, `item.comparacoes.valor.match`, `item.comparacoes.valor.release`, `item.finpet`, `item.finpet.anticipate_value`, `item.finpet.authorization_number`, `item.finpet.bank`, `item.finpet.bank_agency`, `item.finpet.beneficiary`, `item.finpet.beneficiary_document`, `item.finpet.beneficiary_type`, `item.finpet.beneficiary_value`, `item.finpet.client_name`, `item.finpet.client_phone`, `item.finpet.collection_id`, `item.finpet.collection_name`, `item.finpet.cpf`, `item.finpet.created`, `item.finpet.currency`, `item.finpet.date_estimated`, `item.finpet.date_received`, `item.finpet.deposit_account`, `item.finpet.deposit_value`, `item.finpet.discounted_value`, `item.finpet.due_date`, `item.finpet.expand`, `item.finpet.fee`, `item.finpet.gross_value`, `item.finpet.has_chargeback`, `item.finpet.has_contract_applied`, `item.finpet.id`, `item.finpet.id_t`, `item.finpet.installment_number`, `item.finpet.installment_value`, `item.finpet.is_blocked`, `item.finpet.last_four_card_digits`, `item.finpet.merchant`, `item.finpet.merchant_document`, `item.finpet.merchant_user_email`, `item.finpet.not_anticipatable`, `item.finpet.nsu`, `item.finpet.payed_value`, `item.finpet.payment_brand`, `item.finpet.plan_type`, `item.finpet.processor`, `item.finpet.product`, `item.finpet.receipt_id`, `item.finpet.retention_reason`, `item.finpet.retention_value`, `item.finpet.separated_payment_value`, `item.finpet.status`, `item.finpet.transaction_date`, `item.finpet.transaction_number`, `item.finpet.transaction_value`, `item.finpet.type`, `item.finpet.updated`, `item.finpet.ur_external_reference`, `item.finpet.user_name`, `item.finpet.value`, `item.release`, `item.score`

**Opcionais:** `item.comparacoes.auth.auths_encontrados (96%)`, `item.comparacoes.valor.exact_value (96%)`, `item.release.collection_id (96%)`, `item.release.collection_name (96%)`, `item.release.created (96%)`, `item.release.data (96%)`, `item.release.descricao (96%)`, `item.release.expand (96%)`, `item.release.forma_pagamento (96%)`, `item.release.fornecedor (96%)`, `item.release.id (96%)`, `item.release.id_r (96%)`, `item.release.origem (96%)`, `item.release.parcela (96%)`, `item.release.status (96%)`, `item.release.tipo (96%)`, `item.release.updated (96%)`, `item.release.valor (96%)`, `item.release.vencimento (96%)`
