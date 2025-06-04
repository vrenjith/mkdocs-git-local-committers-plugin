# mkdocs-git-local-committers-plugin

A MkDocs plugin that displays a list of local Git committers for each documentation page, without requiring GitHub API access.

## Features

- Shows a list of contributors for each page based on local Git history.
- Displays the last commit date for each file.
- No need for GitHub tokens or API access.
- Supports manual addition of contributors via page metadata.
- Easy integration with custom MkDocs themes.

## Installation

Install the plugin using pip:

```sh
pip install mkdocs-git-local-committers-plugin
```

## Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - git-local-committers
```

**Options:**

| Option         | Description                                                      | Default   |
| -------------- | ---------------------------------------------------------------- | --------- |
| `branch`       | The branch to read commit history from                           | `master`  |
| `max_count`    | Maximum number of commits to scan per file                       | `100`     |
| `exclude`      | List of glob patterns to exclude files from committers analysis  | `[]`      |

Example:

```yaml
plugins:
  - git-local-committers:
      branch: main
      max_count: 200
      exclude:
        - docs/legacy/*
```

## Usage

### Displaying Committers in Templates

The plugin injects a `committers` variable into each page's context, containing a list of contributors for that file. Each committer has:

- `name`: Committer's name
- `email`: Committer's email
- `avatar`: Gravatar URL (if available)

Example (Jinja2):

```django
<ul class="committers">
  {% for user in committers %}
    <li>
      <img src="{{ user.avatar }}" alt="{{ user.name }}" width="24" height="24">
      {{ user.name }}
    </li>
  {% endfor %}
</ul>
```

### Displaying Last Commit Date

The plugin also provides a `last_commit` variable with details about the most recent commit for the page:

- `date`: Commit date (datetime object)
- `message`: Commit message
- `name`: Committer's name
- `email`: Committer's email

Example:

```django
<p>Last updated: {{ last_commit.date.strftime('%Y-%m-%d') }}</p>
```

### Manually Adding Contributors

To credit additional contributors not present in the Git history, add a `contributors` field to your page's YAML metadata:

```yaml
contributors:
  - Alice Example
  - bob@example.com
```

These contributors will be merged with the detected committers.

## Notes

- The plugin requires the documentation source to be in a Git repository.
- No network access or GitHub credentials are needed.
- For best results, ensure your Git history is not shallow (avoid `--depth` clones).

## Acknowledgements

Inspired by the original [mkdocs-git-committers-plugin](https://github.com/byrnereese/mkdocs-git-committers-plugin).

---

For more information on MkDocs plugins, see the [MkDocs documentation](https://www.mkdocs.org/user-guide/plugins/).
