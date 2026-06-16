SELECT
ticker,
account,
shares::numeric as shares,
purchase_price :: numeric as purchase_price,
purchase_date:: date as purchase_date

from {{ source('public', 'portfolio') }}

