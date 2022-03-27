mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor='#9A0680'
backgroundColor='#041C32'
secondaryBackgroundColor='#064663'
textColor='#ECB365'
" > ~/.streamlit/config.toml
