import { Card } from '../ui/Card'
import type { MemeItem } from '../../types/dashboard'

interface MemeCardProps {
  meme: MemeItem
}

export function MemeCard({ meme }: MemeCardProps) {
  return (
    <Card title="Crypto Meme" subtitle="A lighter moment from the crypto world">
      <div className="meme-card">
        <h3 className="meme-card__title">{meme.title}</h3>
        <img
          className="meme-card__image"
          src={meme.image_url}
          alt={meme.title}
        />
        <div className="tag-list">
          {meme.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </Card>
  )
}
