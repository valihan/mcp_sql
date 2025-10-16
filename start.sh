docker run -d --name mcp_sql -p 8101:8101 \
  -v /var/log/mcp:/var/log/mcp \
  -v /data:/app \
  -e BASEURL="http://vhcalnplci:8000/sap/zsql" \
  -e CLIENT="001" \
  -e USERNAME="TEST" \
  -e PASSWORD="tester" \
  -e TOKEN="topsecret" \
  -e LISTEN_HOST="127.0.0.1" \
  -e LISTEN_PORT=8101 \
  mcp_sql
