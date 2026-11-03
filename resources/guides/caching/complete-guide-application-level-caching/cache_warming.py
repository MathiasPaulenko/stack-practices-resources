def warm_cache():
    popular_users = db.users.find_most_active(limit=1000)
    for user in popular_users:
        cache.set(f"user:{user.id}", user)
    
    configurations = db.configs.find_all()
    for config in configurations:
        cache.set(f"config:{config.key}", config)

# Call on application startup
warm_cache()
