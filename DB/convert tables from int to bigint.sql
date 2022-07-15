
ALTER TABLE zmba_product MODIFY COLUMN id_product bigint(30) auto_increment NOT NULL;
ALTER TABLE zmba_product MODIFY COLUMN id_supplier bigint(30) DEFAULT NULL NULL;
ALTER TABLE zmba_product MODIFY COLUMN id_manufacturer bigint(30) DEFAULT NULL NULL;
ALTER TABLE zmba_product MODIFY COLUMN id_category_default bigint(30) DEFAULT NULL NULL;

ALTER TABLE zmba_category MODIFY COLUMN id_category BIGINT(30) auto_increment NOT NULL;
ALTER TABLE zmba_category MODIFY COLUMN id_parent BIGINT(30) NOT NULL;
ALTER TABLE zmba_category MODIFY COLUMN id_shop_default BIGINT(30) DEFAULT 1 NOT NULL;
ALTER TABLE zmba_category_group MODIFY COLUMN id_category bigint(30) unsigned NOT NULL;
ALTER TABLE zmba_category_group MODIFY COLUMN id_group bigint(30) unsigned NOT NULL;
