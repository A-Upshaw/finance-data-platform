with daily_portfolio as (
    SELECT
        ph.date,
        sum(p.shares*ph.close) as portfolio_value
    FROM {{ ref('stg_portfolio') }} p
    join {{ ref('stg_price_history') }} ph on p.ticker = ph.ticker
    group by ph.date
),
spy_daily_price as (
    select 
        ticker,
        close,
        date
    from {{ ref('stg_price_history') }}
    where ticker = 'SPY'
),
indexed as (
    select
        df.date,
        df.portfolio_value,
        sdp.close as spy_close,
        (df.portfolio_value / first_value(df.portfolio_value) over (order by df.date)) * 100 as portfolio_idx,
        (sdp.close / first_value(sdp.close) over (order by sdp.date)) * 100 as spy_idx
    from daily_portfolio df
    join spy_daily_price sdp on df.date = sdp.date
)
select 
    *,
    portfolio_idx - spy_idx as alpha
from indexed 