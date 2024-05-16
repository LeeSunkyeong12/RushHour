# Front-End development
## Deployment FE with nginx
### Step 1: Build Your Vue App for Production
In the project directory, run the build command. This will create a dist/ directory with your compiled app.

```sh
$ cd RushHour/FE/app
$ npm run build
```

### Step 2: Configure NGINX
You will need to configure NGINX to point to your Vue app's dist/ directory.
Here’s a basic example of what your NGINX configuration might look like, typically found in /etc/nginx/sites-available/default on Ubuntu/Debian, or /etc/nginx/nginx.conf on CentOS/RHEL.

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name example.com; # Replace with your domain or IP

    root /path/to/your/app/dist; # Point this to your Vue app's dist directory
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```
