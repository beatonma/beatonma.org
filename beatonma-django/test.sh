# Run tests except those that render template views.
# Allow testing of Django-only code without worrying about frontend stuff.
env/bin/pytest --notemplate "$@"
