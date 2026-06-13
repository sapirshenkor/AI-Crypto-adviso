import { Card } from '../ui/Card'
import { EmptyState } from '../ui/EmptyState'
import type { PriceItem } from '../../types/dashboard'

interface PriceCardProps {
  items: PriceItem[]
}

function formatPrice(price: number): string {
  if (price >= 1) {
    return price.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 2,
    })
  }
  return price.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 4,
  })
}

export function PriceCard({ items }: PriceCardProps) {
  return (
    <Card title="Coin Prices" subtitle="Track your selected assets">
      {items.length === 0 ? (
        <EmptyState message="No price data available." />
      ) : (
        <ul className="price-list">
          {items.map((item) => {
            const isPositive = item.change_24h_percent >= 0
            return (
              <li key={item.id} className="price-list__item">
                <div>
                  <p className="price-list__symbol">{item.symbol}</p>
                  <p className="price-list__asset">{item.asset}</p>
                </div>
                <div className="price-list__values">
                  <p className="price-list__price">{formatPrice(item.price_usd)}</p>
                  <p
                    className={`price-list__change ${
                      isPositive
                        ? 'price-list__change--positive'
                        : 'price-list__change--negative'
                    }`}
                  >
                    {isPositive ? '+' : ''}
                    {item.change_24h_percent.toFixed(1)}%
                  </p>
                </div>
              </li>
            )
          })}
        </ul>
      )}
    </Card>
  )
}
