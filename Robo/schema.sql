CREATE TABLE
	`_migrations` (
		file VARCHAR(255) PRIMARY KEY NOT NULL,
		applied INTEGER NOT NULL
	);

CREATE TABLE
	`_params` (
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`value` JSON DEFAULT NULL,
		`created` TEXT DEFAULT (strftime ('%Y-%m-%d %H:%M:%fZ')) NOT NULL,
		`updated` TEXT DEFAULT (strftime ('%Y-%m-%d %H:%M:%fZ')) NOT NULL
	);

CREATE TABLE
	`_collections` (
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`system` BOOLEAN DEFAULT FALSE NOT NULL,
		`type` TEXT DEFAULT "base" NOT NULL,
		`name` TEXT UNIQUE NOT NULL,
		`fields` JSON DEFAULT "[]" NOT NULL,
		`indexes` JSON DEFAULT "[]" NOT NULL,
		`listRule` TEXT DEFAULT NULL,
		`viewRule` TEXT DEFAULT NULL,
		`createRule` TEXT DEFAULT NULL,
		`updateRule` TEXT DEFAULT NULL,
		`deleteRule` TEXT DEFAULT NULL,
		`options` JSON DEFAULT "{}" NOT NULL,
		`created` TEXT DEFAULT (strftime ('%Y-%m-%d %H:%M:%fZ')) NOT NULL,
		`updated` TEXT DEFAULT (strftime ('%Y-%m-%d %H:%M:%fZ')) NOT NULL
	);

CREATE INDEX idx__collections_type on `_collections` (`type`);

CREATE TABLE
	`_mfas` (
		`collectionRef` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`method` TEXT DEFAULT '' NOT NULL,
		`recordRef` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL
	);

CREATE INDEX `idx_mfas_collectionRef_recordRef` ON `_mfas` (`collectionRef`, `recordRef`);

CREATE TABLE
	sqlite_stat1 (tbl, idx, stat);

CREATE TABLE
	sqlite_stat4 (tbl, idx, neq, nlt, ndlt, sample);

CREATE TABLE
	`_otps` (
		`collectionRef` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`password` TEXT DEFAULT '' NOT NULL,
		`recordRef` TEXT DEFAULT '' NOT NULL,
		`sentTo` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL
	);

CREATE INDEX `idx_otps_collectionRef_recordRef` ON `_otps` (`collectionRef`, `recordRef`);

CREATE TABLE
	`_externalAuths` (
		`collectionRef` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`provider` TEXT DEFAULT '' NOT NULL,
		`providerId` TEXT DEFAULT '' NOT NULL,
		`recordRef` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL
	);

CREATE UNIQUE INDEX `idx_externalAuths_record_provider` ON `_externalAuths` (`collectionRef`, `recordRef`, `provider`);

CREATE UNIQUE INDEX `idx_externalAuths_collection_provider` ON `_externalAuths` (`collectionRef`, `provider`, `providerId`);

CREATE TABLE
	`_authOrigins` (
		`collectionRef` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`fingerprint` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`recordRef` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL
	);

CREATE UNIQUE INDEX `idx_authOrigins_unique_pairs` ON `_authOrigins` (`collectionRef`, `recordRef`, `fingerprint`);

CREATE TABLE
	`_superusers` (
		`created` TEXT DEFAULT '' NOT NULL,
		`email` TEXT DEFAULT '' NOT NULL,
		`emailVisibility` BOOLEAN DEFAULT FALSE NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`password` TEXT DEFAULT '' NOT NULL,
		`tokenKey` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		`verified` BOOLEAN DEFAULT FALSE NOT NULL
	);

CREATE UNIQUE INDEX `idx_tokenKey_pbc_3142635823` ON `_superusers` (`tokenKey`);

CREATE UNIQUE INDEX `idx_email_pbc_3142635823` ON `_superusers` (`email`)
WHERE
	`email` != '';

CREATE TABLE
	`brands` (
		`brand` TEXT DEFAULT '' NOT NULL,
		`brand_simplesvet` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`destination_account` TEXT DEFAULT '' NOT NULL,
		`gateway` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`info` TEXT DEFAULT '' NOT NULL,
		`type` TEXT DEFAULT '' NOT NULL,
		`type_simplesvet` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		"brand_stone" TEXT DEFAULT '' NOT NULL
	);

CREATE TABLE
	`conciliations` (
		`arredondamento` NUMERIC DEFAULT 0 NOT NULL,
		`bandeira` TEXT DEFAULT '' NOT NULL,
		`conta_destino` TEXT DEFAULT '' NOT NULL,
		`conta_origem` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`data` TEXT DEFAULT '' NOT NULL,
		`descricao` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`id_c` TEXT DEFAULT '' NOT NULL,
		`incluido_em` TEXT DEFAULT '' NOT NULL,
		`observacao` TEXT DEFAULT '' NOT NULL,
		`operadora` TEXT DEFAULT '' NOT NULL,
		`status` TEXT DEFAULT '' NOT NULL,
		`taxa_aluguel` NUMERIC DEFAULT 0 NOT NULL,
		`taxa_antecipacao` NUMERIC DEFAULT 0 NOT NULL,
		`taxa_antecipacao_pct` NUMERIC DEFAULT 0 NOT NULL,
		`taxa_bandeira` NUMERIC DEFAULT 0 NOT NULL,
		`taxa_bandeira_pct` NUMERIC DEFAULT 0 NOT NULL,
		`tipo` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		`valor` NUMERIC DEFAULT 0 NOT NULL
	);

CREATE TABLE
	`finpet` (
		`anticipate_value` NUMERIC DEFAULT 0 NOT NULL,
		`authorization_number` TEXT DEFAULT '' NOT NULL,
		`bank` TEXT DEFAULT '' NOT NULL,
		`bank_agency` TEXT DEFAULT '' NOT NULL,
		`beneficiary` TEXT DEFAULT '' NOT NULL,
		`beneficiary_document` TEXT DEFAULT '' NOT NULL,
		`beneficiary_type` TEXT DEFAULT '' NOT NULL,
		`beneficiary_value` NUMERIC DEFAULT 0 NOT NULL,
		`client_name` TEXT DEFAULT '' NOT NULL,
		`client_phone` TEXT DEFAULT '' NOT NULL,
		`cpf` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`currency` TEXT DEFAULT '' NOT NULL,
		`date_estimated` TEXT DEFAULT '' NOT NULL,
		`date_received` TEXT DEFAULT '' NOT NULL,
		`deposit_account` TEXT DEFAULT '' NOT NULL,
		`deposit_value` NUMERIC DEFAULT 0 NOT NULL,
		`discounted_value` NUMERIC DEFAULT 0 NOT NULL,
		`due_date` TEXT DEFAULT '' NOT NULL,
		`fee` NUMERIC DEFAULT 0 NOT NULL,
		`gross_value` NUMERIC DEFAULT 0 NOT NULL,
		`has_chargeback` BOOLEAN DEFAULT FALSE NOT NULL,
		`has_contract_applied` BOOLEAN DEFAULT FALSE NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`id_t` TEXT DEFAULT '' NOT NULL,
		`installment_number` TEXT DEFAULT '' NOT NULL,
		`installment_value` NUMERIC DEFAULT 0 NOT NULL,
		`is_blocked` BOOLEAN DEFAULT FALSE NOT NULL,
		`last_four_card_digits` TEXT DEFAULT '' NOT NULL,
		`merchant` TEXT DEFAULT '' NOT NULL,
		`merchant_document` TEXT DEFAULT '' NOT NULL,
		`merchant_user_email` TEXT DEFAULT '' NOT NULL,
		`not_anticipatable` BOOLEAN DEFAULT FALSE NOT NULL,
		`nsu` TEXT DEFAULT '' NOT NULL,
		`payed_value` NUMERIC DEFAULT 0 NOT NULL,
		`payment_brand` TEXT DEFAULT '' NOT NULL,
		`plan_type` TEXT DEFAULT '' NOT NULL,
		`processor` TEXT DEFAULT '' NOT NULL,
		`product` TEXT DEFAULT '' NOT NULL,
		`receipt_id` TEXT DEFAULT '' NOT NULL,
		`retention_reason` TEXT DEFAULT '' NOT NULL,
		`retention_value` NUMERIC DEFAULT 0 NOT NULL,
		`separated_payment_value` NUMERIC DEFAULT 0 NOT NULL,
		`status` TEXT DEFAULT '' NOT NULL,
		`transaction_date` TEXT DEFAULT '' NOT NULL,
		`transaction_number` TEXT DEFAULT '' NOT NULL,
		`transaction_value` NUMERIC DEFAULT 0 NOT NULL,
		`type` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		`ur_external_reference` TEXT DEFAULT '' NOT NULL,
		`user_name` TEXT DEFAULT '' NOT NULL,
		`value` NUMERIC DEFAULT 0 NOT NULL
	);

CREATE TABLE
	`releases` (
		`created` TEXT DEFAULT '' NOT NULL,
		`data` TEXT DEFAULT '' NOT NULL,
		`descricao` TEXT DEFAULT '' NOT NULL,
		`forma_pagamento` TEXT DEFAULT '' NOT NULL,
		`fornecedor` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`id_r` TEXT DEFAULT '' NOT NULL,
		`origem` TEXT DEFAULT '' NOT NULL,
		`parcela` TEXT DEFAULT '' NOT NULL,
		`status` TEXT DEFAULT '' NOT NULL,
		`tipo` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		`valor` NUMERIC DEFAULT 0 NOT NULL,
		`vencimento` TEXT DEFAULT '' NOT NULL
	);

CREATE UNIQUE INDEX `idx_4okT3oAEpA` ON `releases` (`id_r`);

CREATE TABLE
	`sicoob` (
		`cpf_cnpj` TEXT DEFAULT '' NOT NULL,
		`created` TEXT DEFAULT '' NOT NULL,
		`data` TEXT DEFAULT '' NOT NULL,
		`data_lote` TEXT DEFAULT '' NOT NULL,
		`desc_inf_complementar` TEXT DEFAULT '' NOT NULL,
		`descricao` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`numero_documento` TEXT DEFAULT '' NOT NULL,
		`tipo` TEXT DEFAULT '' NOT NULL,
		`transaction_id` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		`valor` NUMERIC DEFAULT 0 NOT NULL
	);

CREATE UNIQUE INDEX `idx_2h9GMGQs1y` ON `sicoob` (`transaction_id`);

CREATE UNIQUE INDEX `idx_zEUcrkEMbD` ON `brands` (`info`);

CREATE TABLE
	`payments` (
		`created` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`sicoob_payment` TEXT DEFAULT '' NOT NULL,
		`simplesvet_payment` TEXT DEFAULT '' NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL
	);

CREATE TABLE
	IF NOT EXISTS "returns" (
		`created` TEXT DEFAULT '' NOT NULL,
		`id` TEXT PRIMARY KEY DEFAULT ('r' || lower(hex (randomblob (7)))) NOT NULL,
		`updated` TEXT DEFAULT '' NOT NULL,
		"description_return" TEXT DEFAULT '' NOT NULL,
		"description_payment" TEXT DEFAULT '' NOT NULL
	);