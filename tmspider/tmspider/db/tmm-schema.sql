
create table MODEL_INFO(
  STAGE integer,
  UID integer,
  NAME text,
  BIRTH_DATE text,
  HEIGHT numeric(5,1),
  WEIGHT numeric(5,1),
  WAIST  numeric(5,1),
  BUST   numeric(5,1),
  HIP    numeric(5,1),
  CUP    char(1),
  primary key (STAGE, UID)
  );

create table STAGE_NUM (
  NEXT_STAGE int
);
  
  
