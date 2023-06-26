### vietnam bot
# install modules

  1. `sudo apt install python3.9`
  2. `python -m pip install Django`
  3. `pip install pyTelegramBotAPI`
  4. `pip install vardump`



# Test
` 
  1. Install: `git clone git@github.com:raccoon464/vietnam.git`
  2. Change config: `/var/www/vietnam/t_bot/config/main.py`
  3. Start test: `/var/www/vietnam python3 manage.py bot`
  4. Try to send "/start" in your bot
`
   
# Work version
1. Сonfigure nginx.conf (направляем домен на порт 8000)
```
server {
        server_name your-domain.com;
        location /
        {
               proxy_pass http://localhost:8000;
               proxy_buffering off;
               proxy_pass_request_headers on;
               proxy_set_header Connection "Keep-Alive";
               proxy_set_header X-Real-IP  $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header Host $host;
               proxy_set_header X-Forwarded-Proto $scheme;
               proxy_set_header X-Forwarded-Port $server_port;
               proxy_set_header Upgrade $http_upgrade;
               proxy_set_header Connection "upgrade";
    }
}
```
2. Change in  /var/www/vietnam/t_bot/config/main.py url ~~ vietnam.cryptayls.com ~~ => your-domain.com
3. Change in /var/www/vietnam/vietnam/setings.py ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
4. Comand: `python3 manage.py runserver 0.0.0.0:8000`
5. Сheck your url your-domain.com/admin
6. Log in (user = admin/ pass = admin)
7. If it was success, next comand: `/var/www/vietnam python3 manage.py wh`
8. Finish
