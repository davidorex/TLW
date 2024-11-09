# Docker Development Instructions

## Premises
- The development environment should closely mimic the production environment to catch environment-specific issues early.
- Use Docker to containerize the application, ensuring consistency across development and production.

## Goals
- Set up a development environment using Docker with Nginx, Gunicorn, and PostgreSQL.
- Ensure the application runs smoothly in both development and production environments.

## Instructions

### 1. Install Docker on the Remote Server
```bash
# Update package information
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### 2. Transfer Project Files to the Remote Server
```bash
# Use scp to copy files to the remote server
scp -r /path/to/your/project user@remote_host:/path/to/destination
```

### 3. Set Up Environment Variables on the Remote Server
```bash
# Create a .env file with the necessary environment variables
echo "DEBUG=0
SECRET_KEY=GcZRE2eams_3qEAec_KyMh_lTlFA4U5RJzy8w-S2QRHmsuPqAqbd_vX7y3ani6AdqP8
DATABASE_NAME=twl
DATABASE_USER=socrates
DATABASE_PASSWORD=mimnug-qunkUj-gosse8
DATABASE_HOST=db
DATABASE_PORT=5432
ALLOWED_HOSTS=tlw.davidorex.ai" > /path/to/destination/.env
```

### 4. Build and Run Docker Containers
```bash
# Navigate to the project directory
cd /path/to/destination

# Build and start the Docker containers
docker-compose up --build -d
```

### 5. Configure Domain and SSL (Optional)
```bash
# Use Certbot to obtain an SSL certificate
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d tlw.davidorex.ai
```

### 6. Monitor Docker Containers
```bash
# List running Docker containers
docker ps

# View logs for a specific container
docker logs <container_id>
```

## Best Practices
- Use environment variables for configuration management.
- Regularly update dependencies to patch security vulnerabilities.
- Implement logging and monitoring for error tracking and performance metrics.
- Ensure `DEBUG` is set to `False` in production to enhance security.

## Status and Next Steps
- The Docker environment is set up with the necessary configurations.
- Next steps include testing the application in the Docker environment and deploying to production.
