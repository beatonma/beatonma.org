location = /health-check/ {
    add_header Content-Type text/plain;
    return 200 "I am alive";
}
