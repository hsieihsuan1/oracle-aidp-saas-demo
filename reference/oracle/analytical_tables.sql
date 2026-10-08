-- Architectural reference only. Not executed or verified against Oracle.
-- Synthetic analytical tables, not vendor-supported ERP schemas.

-- ============================================================
-- TABELAS JD EDWARDS
-- ============================================================

-- F0006: Business Units (Filiais)
CREATE TABLE JDE_BUSINESS_UNIT (
  MCCO   VARCHAR2(5)   NOT NULL,  -- Company
  MCMCU  VARCHAR2(12)  NOT NULL,  -- Business Unit
  MCDL01 VARCHAR2(40),            -- Description
  MCTYP  VARCHAR2(3),             -- Type
  CONSTRAINT PK_JDE_BU PRIMARY KEY (MCMCU)
);

COMMENT ON TABLE JDE_BUSINESS_UNIT IS 'F0006 - Business Units / Filiais';
COMMENT ON COLUMN JDE_BUSINESS_UNIT.MCMCU IS 'Business Unit (Branch Plant)';
COMMENT ON COLUMN JDE_BUSINESS_UNIT.MCDL01 IS 'Description';

-- F4101: Item Master (Cadastro de Itens)
CREATE TABLE JDE_ITEMS (
  IMITM  NUMBER(8)     NOT NULL,  -- Item Number (Short)
  IMLITM VARCHAR2(25),            -- 2nd Item Number
  IMAITM VARCHAR2(25),            -- 3rd Item Number
  IMDSC1 VARCHAR2(30),            -- Description Line 1
  IMDSC2 VARCHAR2(30),            -- Description Line 2
  IMSRTX VARCHAR2(10),            -- Search Text
  IMUOM  VARCHAR2(2),             -- Primary UoM
  IMGLPT VARCHAR2(4),             -- G/L Class
  IMSTKT VARCHAR2(1),             -- Stocking Type
  CONSTRAINT PK_JDE_ITEMS PRIMARY KEY (IMITM)
);

COMMENT ON TABLE JDE_ITEMS IS 'F4101 - Item Master';
COMMENT ON COLUMN JDE_ITEMS.IMITM IS 'Item Number (Short)';
COMMENT ON COLUMN JDE_ITEMS.IMDSC1 IS 'Item Description';

-- F41021: Item Branch/Plant (Saldo por Filial)
CREATE TABLE JDE_ITEM_BALANCE (
  IBITM  NUMBER(8)     NOT NULL,  -- Item Number
  IBMCU  VARCHAR2(12)  NOT NULL,  -- Branch/Plant
  IBLOTN VARCHAR2(30),            -- Lot Number
  IBLOC  VARCHAR2(20),            -- Location
  IBPQOH NUMBER(15,4),            -- Primary QOH
  IBUOM  VARCHAR2(2),             -- UoM
  IBSAFETY NUMBER(15,4),          -- Safety Stock
  IBREORDER NUMBER(15,4),         -- Reorder Point
  CONSTRAINT PK_JDE_BAL PRIMARY KEY (IBITM, IBMCU, IBLOC)
);

COMMENT ON TABLE JDE_ITEM_BALANCE IS 'F41021 - Item Branch/Plant Balance';
COMMENT ON COLUMN JDE_ITEM_BALANCE.IBPQOH IS 'Quantity On Hand';

-- F4301: Purchase Order Header
CREATE TABLE JDE_PO_HEADER (
  PHDOCO NUMBER(8)    NOT NULL,  -- Order Number
  PHDCTO VARCHAR2(2),            -- Order Type
  PHKCOO VARCHAR2(5),            -- Company
  PHVEND NUMBER(8),              -- Supplier Address Number
  PHTRDJ NUMBER(6),              -- Order Date (CYYDDD)
  PHDRQJ NUMBER(6),              -- Requested Date
  PHST   VARCHAR2(2),            -- Status
  PHCO   VARCHAR2(5),            -- Company
  CONSTRAINT PK_JDE_POH PRIMARY KEY (PHDOCO, PHDCTO)
);

COMMENT ON TABLE JDE_PO_HEADER IS 'F4301 - Purchase Order Header';

-- F4311: Purchase Order Detail
CREATE TABLE JDE_PO_DETAIL (
  PDDOCO NUMBER(8)    NOT NULL,  -- Order Number
  PDDCTO VARCHAR2(2),            -- Order Type
  PDLNID NUMBER(6,3)  NOT NULL,  -- Line Number
  PDITM  NUMBER(8),              -- Item Number
  PDMCU  VARCHAR2(12),           -- Branch/Plant
  PDUORG NUMBER(15,4),           -- Quantity Ordered
  PDUOPN NUMBER(15,4),           -- Quantity Open
  PDPRRC NUMBER(15,4),           -- Unit Cost
  PDAOPN NUMBER(15,4),           -- Amount Open
  PDST   VARCHAR2(2),            -- Line Status
  CONSTRAINT PK_JDE_POD PRIMARY KEY (PDDOCO, PDDCTO, PDLNID)
);

COMMENT ON TABLE JDE_PO_DETAIL IS 'F4311 - Purchase Order Detail';

-- Synthetic work order header; deliberately NOT a certified JDE table mapping.
CREATE TABLE JDE_WO_HEADER (
  WADOCO NUMBER(8)    NOT NULL,  -- Work Order Number
  WADCTO VARCHAR2(2),            -- Order Type
  WADRQJ NUMBER(6),              -- Requested Date
  WASTRT NUMBER(6),              -- Start Date
  WAITMK NUMBER(8),              -- Item Number
  WAMCU  VARCHAR2(12),           -- Branch/Plant
  WAUORG NUMBER(15,4),           -- Quantity Ordered
  WAWQTY NUMBER(15,4),           -- Work Order Quantity
  WACMPL NUMBER(15,4),           -- Quantity Completed
  WAST   VARCHAR2(2),            -- Status
  CONSTRAINT PK_JDE_WO PRIMARY KEY (WADOCO, WADCTO)
);

COMMENT ON TABLE JDE_WO_HEADER IS 'Synthetic Work Order Header (not a certified ERP mapping)';

-- ============================================================
-- TABELAS FUSION ERP (simuladas)
-- ============================================================

-- GL Journals (Lançamentos Contábeis)
CREATE TABLE FUSION_GL_JOURNAL (
  JOURNAL_ID       NUMBER         NOT NULL,
  LEDGER_NAME      VARCHAR2(50),
  PERIOD_NAME      VARCHAR2(20),
  ACCOUNT_CODE     VARCHAR2(30),
  ACCOUNT_DESC     VARCHAR2(100),
  DEBIT_AMOUNT     NUMBER(18,2)   DEFAULT 0,
  CREDIT_AMOUNT    NUMBER(18,2)   DEFAULT 0,
  CURRENCY_CODE    VARCHAR2(3)    DEFAULT 'BRL',
  STATUS           VARCHAR2(20),
  POSTED_DATE      DATE,
  CREATED_BY       VARCHAR2(50),
  CONSTRAINT PK_GL_JOURNAL PRIMARY KEY (JOURNAL_ID)
);

COMMENT ON TABLE FUSION_GL_JOURNAL IS 'Fusion ERP - GL Journals (Lançamentos Contábeis)';

-- AP Invoices (Notas Fiscais a Pagar)
CREATE TABLE FUSION_AP_INVOICES (
  INVOICE_ID       NUMBER         NOT NULL,
  SUPPLIER_NAME    VARCHAR2(100),
  SUPPLIER_NUMBER  VARCHAR2(30),
  INVOICE_NUMBER   VARCHAR2(50),
  INVOICE_DATE     DATE,
  DUE_DATE         DATE,
  AMOUNT           NUMBER(18,2),
  AMOUNT_PAID      NUMBER(18,2)   DEFAULT 0,
  AMOUNT_REMAINING NUMBER(18,2),
  CURRENCY_CODE    VARCHAR2(3)    DEFAULT 'BRL',
  STATUS           VARCHAR2(30),  -- UNPAID, PARTIAL, PAID, OVERDUE
  PAYMENT_TERMS    VARCHAR2(30),
  CONSTRAINT PK_AP_INVOICES PRIMARY KEY (INVOICE_ID)
);

COMMENT ON TABLE FUSION_AP_INVOICES IS 'Fusion ERP - AP Invoices (Contas a Pagar)';
