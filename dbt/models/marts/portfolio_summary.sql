SELECT
    sum(current_value) as total_market_value,
    sum(cost_basis) as total_cost_basis,
    sum(unrealized_gain_loss) as total_gain_loss_dollars,
    round((sum(unrealized_gain_loss) / sum(cost_basis)) * 100, 2) as portfolio_gain_loss_pct

from {{ ref('portfolio_positions') }}