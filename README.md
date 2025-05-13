# beatonma.org

This is the source for my site, [beatonma.org](https://beatonma.org).

The backend uses [Django](https://www.djangoproject.com), [PostgreSQL](https://postgreql.org), [Celery](https://docs.celeryq.dev) and [Redis](https://redis.io) on the back end. The front end is build with [NextJS](https://nextjs.org), [Typescript](https://typescriptlang.org), [React](https://reactjs.org) and [Tailwind](https://tailwindcss.com). [Nginx](https://www.nginx.com) and [Docker Compose](https://github.com/docker/compose) tie it all together.

[beatonma.org](https://beatonma.org) is built with the [indieweb](https://indieweb.org) in mind. It supports [microformats](https://microformats.org) and [webmentions](https://indieweb.org/Webmention) (via my django library, [django-wm](https://github.com/beatonma/django-wm)).


---
## Deployment

### Development
- Populate `.env.dev` using `example.env` as a template.
- Run `./bma dev up --watch`
- Open `localhost:3001` (next.js with autorefresh), `localhost:8001` (django) or `localhost:81` (nginx) in your browser.

### Tests
- Run `./bma test` to run all unit tests and (Cypress) end-to-end tests.
- Run `./bma test unit` to run unit tests for Django and Next.js.
- Django unit tests are run automatically during server startup.

### Complete installation
See [here](tools/install/README.md) for instructions to install the project on a public host.
