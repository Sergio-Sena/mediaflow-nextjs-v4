interface UserCardProps {
  userId: string
  name: string
  avatar: string
  onClick: () => void
}

export default function UserCard({ userId, name, avatar, onClick }: UserCardProps) {
  return (
    <div
      onClick={onClick}
      className="glass-card p-8 text-center cursor-pointer hover:scale-105 hover:border-neon-cyan transition-all duration-300 group"
    >
      <div className="text-7xl mb-4 group-hover:scale-110 transition-transform duration-300">
        {avatar}
      </div>
      <h3 className="text-2xl font-semibold text-white mb-2 group-hover:text-neon-cyan transition-colors">
        {name}
      </h3>
      <p className="text-sm text-gray-400">Clique para acessar</p>
      <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500">
        <span>🔐</span>
        <span>Requer 2FA</span>
      </div>
    </div>
  )
}
