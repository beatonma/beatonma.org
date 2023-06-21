location ~* \.(bash_history|exe|dat|db|env|gz|html|log|php|rar|sql|sqlite|sqlite3|tar|txt|xml|zip)$ {
    return 444;
}
