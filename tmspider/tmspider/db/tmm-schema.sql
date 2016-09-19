
CREATE TABLE model_info(
  stage INTEGER,
  uid INTEGER,
  name TEXT,
  birth_date TEXT,
  height NUMERIC(5,1),
  weight NUMERIC(5,1),
  waist  NUMERIC(5,1),
  bust   NUMERIC(5,1),
  hip    NUMERIC(5,1),
  cup    CHAR(1),
  PRIMARY KEY (stage, uid)
  );

CREATE TABLE stage_num (
  next_stage INT
);
  
  
CREATE OR REPLACE FUNCTION insert_model(
  stage integer,
  uid INTEGER,
  name TEXT,
  birth_date TEXT,
  height NUMERIC(5,1),
  weight NUMERIC(5,1),
  waist  NUMERIC(5,1),
  bust   NUMERIC(5,1),
  hip    NUMERIC(5,1),
  cup    CHAR(1)
) RETURNS VOID AS $$
BEGIN
 INSERT INTO model_info
   (stage, uid, name, birth_date, height, weight, waist, bust, hip, cup)
 VALUES
  (stage, uid, name, birth_date, height, weight, waist, bust, hip, cup);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_stage_num() RETURNS int AS $$
DECLARE
  n int;
BEGIN
 SELECT next_stage INTO n
   FROM stage_num
   LIMIT 1;
 UPDATE stage_num
    SET next_stage = next_stage + 1;
 return n;
END;
$$ LANGUAGE plpgsql;


       

       
