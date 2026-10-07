USE FinancialDataPipeline;
GO

CREATE TABLE dbo.transactions
(
    transaction_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    state VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    merchant VARCHAR(100) NOT NULL,

    CONSTRAINT PK_transactions
        PRIMARY KEY (transaction_id)
);
GO