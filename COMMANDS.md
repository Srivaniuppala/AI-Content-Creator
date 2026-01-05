# Docker Commands Reference

## Service Management

### Start all services
```bash
docker-compose up -d
```

### Stop all services
```bash
docker-compose down
```

### Restart all services
```bash
docker-compose restart
```

### Restart specific service
```bash
docker-compose restart streamlit
docker-compose restart postgres
```

### View service status
```bash
docker-compose ps
```

### Stop and remove all data (⚠️ destructive)
```bash
docker-compose down -v
```

---

## Logs and Debugging

### View logs from all services
```bash
docker-compose logs -f
```

### View logs from specific service
```bash
docker-compose logs -f streamlit
docker-compose logs -f postgres
```

### View last 100 lines
```bash
docker-compose logs --tail=100
```

### View logs without following
```bash
docker-compose logs streamlit
```

---

## Database Operations

### Connect to PostgreSQL
```bash
docker exec -it content_creator_db psql -U content_admin -d content_creator
```

### Backup database
```bash
docker exec content_creator_db pg_dump -U content_admin content_creator > backup.sql
```

### Restore database
```bash
cat backup.sql | docker exec -i content_creator_db psql -U content_admin -d content_creator
```

### View database tables
```sql
-- After connecting to psql
\dt
```

### View table structure
```sql
\d users
\d generated_content
```

### Check database size
```sql
SELECT pg_size_pretty(pg_database_size('content_creator'));
```

---

## Groq API Testing

### Test API connection
```bash
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hello"}]}'
```

### Check available models
Available models:
- `llama-3.3-70b-versatile` (Default, best performance)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

### Update API key in .env
```bash
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Container Management

### Execute command in container
```bash
docker exec -it content_creator_app bash
docker exec -it content_creator_db bash
```

### View container resource usage
```bash
docker stats
```

### Inspect container
```bash
docker inspect content_creator_app
```

### View container processes
```bash
docker top content_creator_app
```

---

## Cleanup Commands

### Remove stopped containers
```bash
docker container prune
```

### Remove unused images
```bash
docker image prune -a
```

### Remove unused volumes
```bash
docker volume prune
```

### Remove everything (⚠️ nuclear option)
```bash
docker system prune -a --volumes
```

---

## Troubleshooting Commands

### Check Docker disk usage
```bash
docker system df
```

### View Docker network
```bash
docker network ls
docker network inspect sriproject_content_network
```

### Rebuild specific service
```bash
docker-compose up -d --build streamlit
```

### Force recreate containers
```bash
docker-compose up -d --force-recreate
```

### Pull latest images
```bash
docker-compose pull
```

---

## Application-Specific Commands

### Access Python shell in app
```bash
docker exec -it content_creator_app python
```

### Run database migrations (if needed)
```bash
docker exec -it content_creator_app python -c "from database.db import Database; db = Database()"
```

### Check Streamlit version
```bash
docker exec content_creator_app streamlit --version
```

### View app environment variables
```bash
docker exec content_creator_app env
```

---

## Performance Monitoring

### Monitor all containers
```bash
docker stats
```

### Monitor specific container
```bash
docker stats content_creator_app
```

### View container logs with timestamps
```bash
docker logs -t content_creator_app
```

### Check container health
```bash
docker inspect --format='{{.State.Health.Status}}' content_creator_app
```

---

## Development Commands

### Tail logs while developing
```bash
docker-compose logs -f streamlit
```

### Restart after code changes
```bash
docker-compose restart streamlit
```

### Hot reload (mount volume in docker-compose.yml)
```yaml
volumes:
  - ./app:/app
```

### Run tests in container
```bash
docker exec content_creator_app pytest
```

---

## Useful Queries

### Count users
```sql
SELECT COUNT(*) FROM users;
```

### Count generated content
```sql
SELECT COUNT(*) FROM generated_content;
```

### View recent content
```sql
SELECT * FROM generated_content ORDER BY created_at DESC LIMIT 10;
```

### Content by type
```sql
SELECT ct.name, COUNT(gc.id) as count
FROM generated_content gc
JOIN content_types ct ON gc.content_type_id = ct.id
GROUP BY ct.name
ORDER BY count DESC;
```

### Most active users
```sql
SELECT u.email, COUNT(gc.id) as content_count
FROM users u
LEFT JOIN generated_content gc ON u.id = gc.user_id
GROUP BY u.id, u.email
ORDER BY content_count DESC;
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start services |
| `docker-compose down` | Stop services |
| `docker-compose logs -f` | View logs |
| `docker-compose ps` | Service status |
| `docker exec -it <container> bash` | Access container |
| `docker stats` | Monitor resources |

---

## Emergency Recovery

### Services won't start
```bash
docker-compose down
docker system prune -f
docker-compose up -d
```

### Database is corrupted
```bash
docker-compose down
docker volume rm sriproject_postgres_data
docker-compose up -d
```

### App crashes on startup
```bash
docker-compose logs streamlit
docker-compose restart streamlit
```

### Groq API errors
```bash
# Check API key is set
docker exec content_creator_app env | grep GROQ

# Test API connection
curl https://api.groq.com/openai/v1/models -H "Authorization: Bearer YOUR_API_KEY"

# Restart app
docker-compose restart streamlit
```

---

## Tips

1. **Always check logs first**: `docker-compose logs -f`
2. **Use health checks**: Services have built-in health checks
3. **Resource limits**: Monitor with `docker stats`
4. **Regular backups**: Backup database regularly
5. **Clean up**: Run prune commands periodically
6. **Version control**: Don't commit `.env` file with API keys
7. **Security**: Keep API keys secure and rotate regularly
8. **Groq API**: Free tier has rate limits, monitor usage at https://console.groq.com

---

For more help, see:
- [README.md](README.md) - Full documentation
- [SETUP.md](SETUP.md) - Setup guide
- Docker documentation: https://docs.docker.com/
