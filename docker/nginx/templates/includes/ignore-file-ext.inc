location ~* \.(bash_history|exe|dat|db|env|gz|html|log|php|rar|sql|sqlite|sqlite3|tar|zip)$ {
    return 444;
}
