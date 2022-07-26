
/**

                        PRODUCT

**/
DROP TABLE IF EXISTS shalom_product;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product` AS
select
   *
from
    `kitkat_product`;
DROP TABLE IF EXISTS shalom_product_attachment;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_attachment` AS
select
   *
from
    `kitkat_product_attachment`;
DROP TABLE IF EXISTS shalom_product_attribute;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_attribute` AS
select
   *
from
    `kitkat_product_attribute`;
DROP TABLE IF EXISTS shalom_product_attribute_combination;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_attribute_combination` AS
select
   *
from
    `kitkat_product_attribute_combination`;
DROP TABLE IF EXISTS shalom_product_attribute_image;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_attribute_image` AS
select
   *
from
    `kitkat_product_attribute_image`;
DROP TABLE IF EXISTS shalom_product_attribute_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_attribute_shop` AS
select
   *
from
    `kitkat_product_attribute_shop`;
DROP TABLE IF EXISTS shalom_product_carrier;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_carrier` AS
select
   *
from
    `kitkat_product_carrier`;




DROP TABLE IF EXISTS shalom_product_country_tax;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_country_tax` AS
select
   *
from
    `kitkat_product_country_tax`;


DROP TABLE IF EXISTS shalom_product_download;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_download` AS
select
   *
from
    `kitkat_product_download`;

DROP TABLE IF EXISTS shalom_product_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_lang` AS
select
   *
from
    `kitkat_product_lang`;


DROP TABLE IF EXISTS shalom_product_sale;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_sale` AS
select
   *
from
    `kitkat_product_sale`;


DROP TABLE IF EXISTS shalom_product_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_shop` AS
select
   *
from
    `kitkat_product_shop`;


DROP TABLE IF EXISTS shalom_product_supplier;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_supplier` AS
select
   *
from
    `kitkat_product_supplier`;



DROP TABLE IF EXISTS shalom_product_tag;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_product_tag` AS
select
   *
from
    `kitkat_product_tag`;


/**

                        CATEGORY

**/


DROP TABLE IF EXISTS shalom_category;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_category` AS
select
   *
from
    `kitkat_category`;


DROP TABLE IF EXISTS shalom_category_group;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_category_group` AS
select
   *
from
    `kitkat_category_group`;


DROP TABLE IF EXISTS shalom_category_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_category_lang` AS
select
   *
from
    `kitkat_category_lang`;


DROP TABLE IF EXISTS shalom_category_product;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_category_product` AS
select
   *
from
    `kitkat_category_product`;


DROP TABLE IF EXISTS shalom_category_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_category_shop` AS
select
   *
from
    `kitkat_category_shop`;


/** 

CMS



**/

DROP TABLE IF EXISTS shalom_cms;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms` AS
select
   *
from
    `kitkat_cms`;


DROP TABLE IF EXISTS shalom_cms_category;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_category` AS
select
   *
from
    `kitkat_cms_category`;


DROP TABLE IF EXISTS shalom_cms_category_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_category_lang` AS
select
   *
from
    `kitkat_cms_category_lang`;


DROP TABLE IF EXISTS shalom_cms_category_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_category_shop` AS
select
   *
from
    `kitkat_cms_category_shop`;



DROP TABLE IF EXISTS shalom_cms_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_lang` AS
select
   *
from
    `kitkat_cms_lang`;



DROP TABLE IF EXISTS shalom_cms_role;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_role` AS
select
   *
from
    `kitkat_cms_role`;


DROP TABLE IF EXISTS shalom_cms_role_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_role_lang` AS
select
   *
from
    `kitkat_cms_role_lang`;


DROP TABLE IF EXISTS shalom_cms_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_cms_shop` AS
select
   *
from
    `kitkat_cms_shop`;


    
/** 

                                lang



**/
DROP TABLE IF EXISTS shalom_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_lang` AS
select
   *
from
    `kitkat_lang`;

DROP TABLE IF EXISTS shalom_lang_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_lang_shop` AS
select
   *
from
    `kitkat_lang_shop`;


/**
                            zone
*/

DROP TABLE IF EXISTS shalom_zone;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_zone` AS
select
   *
from
    `kitkat_zone`;

DROP TABLE IF EXISTS shalom_state;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_state` AS
select
   *
from
    `kitkat_state`;





/**
                            zone
*/

DROP TABLE IF EXISTS shalom_zone;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_zone` AS
select
   *
from
    `kitkat_zone`;

DROP TABLE IF EXISTS shalom_state;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_state` AS
select
   *
from
    `kitkat_state`;

    

/** 

                                features



**/





DROP TABLE IF EXISTS shalom_feature;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature` AS
select
   *
from
    `kitkat_feature`;


DROP TABLE IF EXISTS shalom_feature_flag;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_flag` AS
select
   *
from
    `kitkat_feature_flag`;

DROP TABLE IF EXISTS shalom_feature_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_lang` AS
select
   *
from
    `kitkat_feature_lang`;


DROP TABLE IF EXISTS shalom_feature_product;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_product` AS
select
   *
from
    `kitkat_feature_product`;


DROP TABLE IF EXISTS shalom_feature_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_shop` AS
select
   *
from
    `kitkat_feature_shop`;

DROP TABLE IF EXISTS shalom_feature_value;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_value` AS
select
   *
from
    `kitkat_feature_value`;

DROP TABLE IF EXISTS shalom_feature_value_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_feature_value_lang` AS
select
   *
from
    `kitkat_feature_value_lang`;


/**



                            stock



*/


DROP TABLE IF EXISTS shalom_stock;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_stock` AS
select
   *
from
    `kitkat_stock`;



DROP TABLE IF EXISTS shalom_stock_available;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_stock_available` AS
select
   *
from
    `kitkat_stock_available`;


DROP TABLE IF EXISTS shalom_stock_mvt;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_stock_mvt` AS
select
   *
from
    `kitkat_stock_mvt`;


DROP TABLE IF EXISTS shalom_stock_mvt_reason;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_stock_mvt_reason` AS
select
   *
from
    `kitkat_stock_mvt_reason`;


DROP TABLE IF EXISTS shalom_stock_mvt_reason_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_stock_mvt_reason_lang` AS
select
   *
from
    `kitkat_stock_mvt_reason_lang`;

/**

tag

**/


DROP TABLE IF EXISTS shalom_tax;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_tax` AS
select
   *
from
    `kitkat_tax`;


 DROP TABLE IF EXISTS shalom_tax_lang;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_tax_lang` AS
select
   *
from
    `kitkat_tax_lang`;

 DROP TABLE IF EXISTS shalom_tax_rule;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_tax_rule` AS
select
   *
from
    `kitkat_tax_rule`;


 DROP TABLE IF EXISTS shalom_tax_rules_group;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_tax_rules_group` AS
select
   *
from
    `kitkat_tax_rules_group`;



DROP TABLE IF EXISTS shalom_tax_rules_group_shop;
CREATE  OR REPLACE
ALGORITHM = UNDEFINED VIEW `shalom_tax_rules_group_shop` AS
select
   *
from
    `kitkat_tax_rules_group_shop`;







    
