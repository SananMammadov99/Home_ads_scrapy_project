ALTER TABLE bina_az
RENAME COLUMN "Description" TO description;
ALTER TABLE bina_az
RENAME COLUMN "Last Updated" TO last_updated;
ALTER TABLE bina_az
RENAME COLUMN "Number of Views" TO number_of_views;
ALTER TABLE bina_az
RENAME COLUMN "Owner Name" TO owner_name;
ALTER TABLE bina_az
RENAME COLUMN "Owner Region" TO owner_region;
ALTER TABLE bina_az
RENAME COLUMN "Shop Owner Name" TO shop_owner_name;
ALTER TABLE bina_az
RENAME COLUMN "Shop Owner Region" TO shop_owner_region;
ALTER TABLE bina_az
RENAME COLUMN "Residence Name" TO residence_name;
ALTER TABLE bina_az
RENAME COLUMN "Residence Region" TO residence_region;
ALTER TABLE bina_az
RENAME COLUMN "Longitude" TO longitude;
ALTER TABLE bina_az
RENAME COLUMN "Latitude" TO latitude;
ALTER TABLE bina_az
RENAME COLUMN "Kateqoriya" TO kateqoriya;
ALTER TABLE bina_az
RENAME COLUMN "Mərtəbə" TO mertebe;
ALTER TABLE bina_az
RENAME COLUMN "Sahə" TO sahe;
ALTER TABLE bina_az
RENAME COLUMN "Otaq sayı" TO otaq_sayi;
ALTER TABLE bina_az
RENAME COLUMN "Çıxarış" TO cixaris;
ALTER TABLE bina_az
RENAME COLUMN "İpoteka" TO ipoteka;
ALTER TABLE bina_az
RENAME COLUMN "Təmir" TO temir;


update bina_az
set price_value = cast(replace(price_value, ' ', '') as int);

alter table bina_az
alter column price_value type integer using (trim(price_value)::integer);

ALTER TABLE bina_az
ADD COLUMN current_floor INTEGER;

ALTER TABLE bina_az
ADD COLUMN total_floors INTEGER;

UPDATE bina_az
SET
    current_floor = CAST(SPLIT_PART(mertebe, '/', 1) AS INTEGER),
    total_floors = CAST(SPLIT_PART(mertebe, '/', 2) AS INTEGER);

ALTER TABLE bina_az
ADD COLUMN area_value NUMERIC;
ALTER TABLE bina_az
ADD COLUMN area_unit VARCHAR(5);

UPDATE bina_az
SET
    area_value = CAST(SPLIT_PART(sahe, ' ', 1) AS NUMERIC),
    area_unit = SPLIT_PART(sahe, ' ', 2);
