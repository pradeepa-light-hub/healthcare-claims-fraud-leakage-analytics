USE ROLE ACCOUNTADMIN;
USE DATABASE HEALTHCARE;
USE SCHEMA RAW;

CREATE OR REPLACE FILE FORMAT HEALTHCARE.RAW.CSV_FMT
    TYPE = 'CSV'

--formatTypeOptions ::=
-- If TYPE = CSV
     COMPRESSION = 'AUTO'
     FIELD_DELIMITER = ','
     FIELD_OPTIONALLY_ENCLOSED_BY = '"'
     SKIP_HEADER = 1
     EMPTY_FIELD_AS_NULL = TRUE
     NULL_IF = ( '','\\N', 'NULL' )
     TRIM_SPACE = FALSE
     ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE

CREATE OR REPLACE STAGE HEALTHCARE.RAW.HEALTHCARE
  STORAGE_INTEGRATION = HEALTHCARE
  URL = 's3://yt-healthcare-claim-fraud-leakage-pipeline-dpp-pidhya/raw/'
  FILE_FORMAT = HEALTHCARE.RAW.CSV_FMT; -- 👈 Add the semicolon right here!

-- Now you can highlight and run this line by itself cleanly!
LIST @HEALTHCARE.RAW.HEALTHCARE;
