SELECT
ticker::text as ticker,
company::text as company,
sector::text as sector,
industry::text as industry,
asset_type::text as asset_type,
exchange::text as exchange

from {{ source('public', 'stocks') }}