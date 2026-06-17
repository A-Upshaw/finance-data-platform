with total as(
    select sum(current_value) as total_portfolio_value 
    from {{ ref('portfolio_positions') }}
)

SELECT
    s.sector,
    sum(current_value) as sector_market_value,
    sum(cost_basis) as sector_cost_basis,
    sum(unrealized_gain_loss) as sector_gain_loss_dollars,
    round((sum(unrealized_gain_loss) / sum(cost_basis)) * 100, 2) as sector_gain_loss_pct,
    round(sum(pp.current_value)/ total.total_portfolio_value * 100,2) as allocation_pct 


From {{ ref('portfolio_positions') }} pp 
left join {{ ref('stg_stocks') }} s on pp.ticker = s.ticker
cross join total 
group by s.sector,total.total_portfolio_value