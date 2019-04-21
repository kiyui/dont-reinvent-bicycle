FROM nginx:stable
COPY nginx /etc/nginx
COPY output /usr/share/nginx/html
