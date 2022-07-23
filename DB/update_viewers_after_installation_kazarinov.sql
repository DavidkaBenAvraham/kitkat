

DROP TABLE IF EXISTS kazarinov_product;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product` AS
select
   *
from
    `dev_product`;
DROP TABLE IF EXISTS kazarinov_product_attachment;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_attachment` AS
select
   *
from
    `dev_product_attachment`;
DROP TABLE IF EXISTS kazarinov_product_attribute;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_attribute` AS
select
   *
from
    `dev_product_attribute`;
DROP TABLE IF EXISTS kazarinov_product_attribute_combination;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_attribute_combination` AS
select
   *
from
    `dev_product_attribute_combination`;
DROP TABLE IF EXISTS kazarinov_product_attribute_image;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_attribute_image` AS
select
   *
from
    `dev_product_attribute_image`;
DROP TABLE IF EXISTS kazarinov_product_attribute_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_attribute_shop` AS
select
   *
from
    `dev_product_attribute_shop`;
DROP TABLE IF EXISTS kazarinov_product_carrier;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_carrier` AS
select
   *
from
    `dev_product_carrier`;








DROP TABLE IF EXISTS kazarinov_product_country_tax;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_country_tax` AS
select
   *
from
    `dev_product_country_tax`;
DROP TABLE IF EXISTS kazarinov_product_download;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_download` AS
select
   *
from
    `dev_product_download`;

DROP TABLE IF EXISTS kazarinov_product_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_lang` AS
select
   *
from
    `dev_product_lang`;
DROP TABLE IF EXISTS kazarinov_product_sale;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_sale` AS
select
   *
from
    `dev_product_sale`;
DROP TABLE IF EXISTS kazarinov_product_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_shop` AS
select
   *
from
    `dev_product_shop`;
DROP TABLE IF EXISTS kazarinov_product_supplier;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_supplier` AS
select
   *
from
    `dev_product_supplier`;
DROP TABLE IF EXISTS kazarinov_product_tag;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `kazarinov_product_tag` AS
select
   *
from
    `dev_product_tag`;







