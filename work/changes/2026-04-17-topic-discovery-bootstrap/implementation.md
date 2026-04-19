# Implementation

- kept the topic page renderer in `src/app/application/use_cases/build_site.py`
- used the shared discovery surface to link from topic pages to archives and
  search
- preserved the existing `/library/<tag>/` destination structure and topic
  body content
- retained the topic discovery assertions in the build and integration tests
