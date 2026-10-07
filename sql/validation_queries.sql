USE FinancialDataPipeline;
GO

-- ============================================
-- SQL DATA QUALITY VALIDATION
-- ============================================


-- ============================================
-- 1. Duplicate Transaction IDs
-- ============================================

SELECT
    transaction_id,
    COUNT(*) AS duplicate_count
FROM dbo.transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;


-- ============================================
-- 2. Missing Values
-- ============================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(transaction_id) AS transaction_id_count,
    COUNT(customer_id) AS customer_id_count,
    COUNT(transaction_date) AS transaction_date_count,
    COUNT(transaction_type) AS transaction_type_count,
    COUNT(category) AS category_count,
    COUNT(amount) AS amount_count,
    COUNT(payment_method) AS payment_method_count,
    COUNT(state) AS state_count,
    COUNT(status) AS status_count,
    COUNT(merchant) AS merchant_count
FROM dbo.transactions;


-- ============================================
-- 3. Invalid Transaction Dates
-- ============================================

SELECT
    COUNT(*) AS invalid_date_count
FROM dbo.transactions
WHERE transaction_date < '2025-01-01'
   OR transaction_date > '2026-09-25';


-- ============================================
-- 4. Invalid Transaction Amounts
-- ============================================

SELECT
    COUNT(*) AS invalid_amount_count
FROM dbo.transactions
WHERE amount <= 0
   OR amount > 5000;



-- ============================================
-- 5. Invalid States
-- ============================================

SELECT
    COUNT(*) AS invalid_state_count
FROM dbo.transactions
WHERE state NOT IN (
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
    'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
    'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS',
    'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
    'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
    'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY',
    'Unknown'
);


-- ============================================
-- 6. Invalid Transaction Statuses
-- ============================================

SELECT
    COUNT(*) AS invalid_status_count
FROM dbo.transactions
WHERE status NOT IN (
    'Completed',
    'Pending',
    'Failed',
    'Reversed',
    'Unknown'
);



-- ============================================
-- 7. Invalid Transaction Types
-- ============================================

SELECT
    COUNT(*) AS invalid_transaction_type_count
FROM dbo.transactions
WHERE transaction_type NOT IN (
    'Debit',
    'Credit'
);



-- ============================================
-- 8. Invalid Categories
-- ============================================

SELECT
    COUNT(*) AS invalid_category_count
FROM dbo.transactions
WHERE category NOT IN (
    'Groceries',
    'Utilities',
    'Dining',
    'Transportation',
    'Healthcare',
    'Entertainment',
    'Shopping',
    'Salary',
    'Transfer',
    'Other',
    'Unknown'
);

-- ============================================
-- 9. Invalid Payment Methods
-- ============================================

SELECT
    COUNT(*) AS invalid_payment_method_count
FROM dbo.transactions
WHERE payment_method NOT IN (
    'Credit Card',
    'Debit Card',
    'ACH',
    'Wire Transfer',
    'Cash',
    'Check',
    'Unknown'
);


-- ============================================
-- 10. Exact Duplicate Records
-- ============================================

SELECT
    transaction_id,
    customer_id,
    transaction_date,
    transaction_type,
    category,
    amount,
    payment_method,
    state,
    status,
    merchant,
    COUNT(*) AS duplicate_count
FROM dbo.transactions
GROUP BY
    transaction_id,
    customer_id,
    transaction_date,
    transaction_type,
    category,
    amount,
    payment_method,
    state,
    status,
    merchant
HAVING COUNT(*) > 1;



-- ============================================
-- SQL DATA QUALITY VALIDATION SUMMARY
-- ============================================

SELECT
    'Duplicate Transaction IDs' AS validation_check,
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM (
    SELECT transaction_id
    FROM dbo.transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
) AS duplicate_ids

UNION ALL

SELECT
    'Missing Values',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE transaction_id IS NULL
   OR customer_id IS NULL
   OR transaction_date IS NULL
   OR transaction_type IS NULL
   OR category IS NULL
   OR amount IS NULL
   OR payment_method IS NULL
   OR state IS NULL
   OR status IS NULL
   OR merchant IS NULL

UNION ALL

SELECT
    'Invalid Dates',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE transaction_date < '2025-01-01'
   OR transaction_date > '2026-09-25'

UNION ALL

SELECT
    'Invalid Amounts',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE amount <= 0
   OR amount > 5000

UNION ALL

SELECT
    'Invalid States',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE state NOT IN (
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
    'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
    'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS',
    'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
    'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
    'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY',
    'Unknown'
)

UNION ALL

SELECT
    'Invalid Statuses',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE status NOT IN (
    'Completed',
    'Pending',
    'Failed',
    'Reversed',
    'Unknown'
)

UNION ALL

SELECT
    'Invalid Transaction Types',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE transaction_type NOT IN (
    'Debit',
    'Credit'
)

UNION ALL

SELECT
    'Invalid Categories',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE category NOT IN (
    'Groceries',
    'Utilities',
    'Dining',
    'Transportation',
    'Healthcare',
    'Entertainment',
    'Shopping',
    'Salary',
    'Transfer',
    'Other',
    'Unknown'
)

UNION ALL

SELECT
    'Invalid Payment Methods',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM dbo.transactions
WHERE payment_method NOT IN (
    'Credit Card',
    'Debit Card',
    'ACH',
    'Wire Transfer',
    'Cash',
    'Check',
    'Unknown'
)

UNION ALL

SELECT
    'Exact Duplicate Records',
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM (
    SELECT
        transaction_id,
        customer_id,
        transaction_date,
        transaction_type,
        category,
        amount,
        payment_method,
        state,
        status,
        merchant
    FROM dbo.transactions
    GROUP BY
        transaction_id,
        customer_id,
        transaction_date,
        transaction_type,
        category,
        amount,
        payment_method,
        state,
        status,
        merchant
    HAVING COUNT(*) > 1
) AS duplicate_records;



-- ============================================
-- OVERALL VALIDATION RESULT
-- ============================================

SELECT
    COUNT(*) AS total_checks,
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) AS checks_passed,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) AS checks_failed,
    CASE
        WHEN SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) = 0
            THEN 'PASS'
        ELSE 'FAIL'
    END AS overall_result
FROM
(
    SELECT
        'Duplicate Transaction IDs' AS validation_check,
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END AS status
    FROM (
        SELECT transaction_id
        FROM dbo.transactions
        GROUP BY transaction_id
        HAVING COUNT(*) > 1
    ) AS duplicate_ids

    UNION ALL

    SELECT
        'Missing Values',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE transaction_id IS NULL
       OR customer_id IS NULL
       OR transaction_date IS NULL
       OR transaction_type IS NULL
       OR category IS NULL
       OR amount IS NULL
       OR payment_method IS NULL
       OR state IS NULL
       OR status IS NULL
       OR merchant IS NULL

    UNION ALL

    SELECT
        'Invalid Dates',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE transaction_date < '2025-01-01'
       OR transaction_date > '2026-09-25'

    UNION ALL

    SELECT
        'Invalid Amounts',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE amount <= 0
       OR amount > 5000

    UNION ALL

    SELECT
        'Invalid States',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE state NOT IN (
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
        'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
        'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS',
        'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
        'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
        'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY',
        'Unknown'
    )

    UNION ALL

    SELECT
        'Invalid Statuses',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE status NOT IN (
        'Completed',
        'Pending',
        'Failed',
        'Reversed',
        'Unknown'
    )

    UNION ALL

    SELECT
        'Invalid Transaction Types',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE transaction_type NOT IN (
        'Debit',
        'Credit'
    )

    UNION ALL

    SELECT
        'Invalid Categories',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE category NOT IN (
        'Groceries',
        'Utilities',
        'Dining',
        'Transportation',
        'Healthcare',
        'Entertainment',
        'Shopping',
        'Salary',
        'Transfer',
        'Other',
        'Unknown'
    )

    UNION ALL

    SELECT
        'Invalid Payment Methods',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM dbo.transactions
    WHERE payment_method NOT IN (
        'Credit Card',
        'Debit Card',
        'ACH',
        'Wire Transfer',
        'Cash',
        'Check',
        'Unknown'
    )

    UNION ALL

    SELECT
        'Exact Duplicate Records',
        CASE
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END
    FROM (
        SELECT
            transaction_id,
            customer_id,
            transaction_date,
            transaction_type,
            category,
            amount,
            payment_method,
            state,
            status,
            merchant
        FROM dbo.transactions
        GROUP BY
            transaction_id,
            customer_id,
            transaction_date,
            transaction_type,
            category,
            amount,
            payment_method,
            state,
            status,
            merchant
        HAVING COUNT(*) > 1
    ) AS duplicate_records
) AS validation_results;

