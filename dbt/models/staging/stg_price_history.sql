select
    ticker,
    date,
    open::numeric    as open,
    high::numeric    as high,
    low::numeric     as low,
    close::numeric   as close,
    volume::bigint   as volume
from {{ source('public', 'price_history') }}
where close is not null
